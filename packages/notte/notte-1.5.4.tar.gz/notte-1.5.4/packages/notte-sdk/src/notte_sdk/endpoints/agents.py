import asyncio
import time
from collections.abc import Sequence
from typing import Any, Callable, Unpack

import websockets
from halo import Halo  # pyright: ignore[reportMissingTypeStubs]
from loguru import logger
from notte_core.actions import CompletionAction
from notte_core.common.config import config
from notte_core.common.notifier import BaseNotifier
from notte_core.utils.webp_replay import WebpReplay
from pydantic import BaseModel
from typing_extensions import final, override

from notte_sdk.endpoints.base import BaseClient, NotteEndpoint
from notte_sdk.endpoints.sessions import RemoteSession, get_context_session_id
from notte_sdk.endpoints.vaults import NotteVault
from notte_sdk.types import (
    DEFAULT_MAX_NB_STEPS,
    AgentCreateRequestDict,
    AgentListRequest,
    AgentListRequestDict,
    AgentResponse,
    AgentRunRequestDict,
    AgentStartRequest,
    AgentStartRequestDict,
    AgentStatus,
    AgentStatusRequest,
    _AgentCreateRequest,  # pyright: ignore[reportPrivateUsage]
    render_agent_status,
)
from notte_sdk.types import AgentStatusResponse as _AgentStatusResponse


# proxy for: StepAgentOutput
class AgentStepResponse(BaseModel):
    state: dict[str, Any]
    actions: list[dict[str, Any]]

    def pretty_string(self, colors: bool = True) -> list[tuple[str, dict[str, str]]]:
        action_str = ""
        actions = self.actions
        for action in actions:
            action_str += f"   ▶ {action}"

        interaction_str = ""
        for interaction in self.state.get("relevant_interactions", []):
            interaction_str += f"\n   ▶ {interaction.get('id')}: {interaction.get('reason')}"

        return render_agent_status(
            status=self.state.get("previous_goal_status", "no agent status"),
            summary=self.state.get("page_summary", "no page summary"),
            goal_eval=self.state.get("previous_goal_eval", "no goal eval"),
            next_goal=self.state.get("next_goal", "no next goal"),
            memory=self.state.get("memory", "no memory"),
            interaction_str=interaction_str,
            action_str=action_str,
            colors=colors,
        )

    def log_pretty_string(self, colors: bool = True) -> None:
        for text, data in self.pretty_string(colors=colors):
            time.sleep(0.1)
            logger.opt(colors=True).info(text, **data)

    def is_done(self) -> bool:
        # check for completion action
        for action in self.actions:
            if action.get("type") == CompletionAction.name():
                return True
        return False


AgentStatusResponse = _AgentStatusResponse[AgentStepResponse]


@final
class AgentsClient(BaseClient):
    """
    Client for the Notte API.

    Note: this client is only able to handle one session at a time.
    If you need to handle multiple sessions, you need to create a new client for each session.
    """

    # Session
    AGENT_START = "start"
    AGENT_START_CUSTOM = "start/custom"
    AGENT_STOP = "{agent_id}/stop"
    AGENT_STATUS = "{agent_id}"
    AGENT_LIST = ""
    # The following endpoints downloads a .webp file
    AGENT_REPLAY = "{agent_id}/replay"
    AGENT_LOGS_WS = "{agent_id}/debug/logs?token={token}"

    def __init__(
        self,
        api_key: str | None = None,
        server_url: str | None = None,
        verbose: bool = False,
    ):
        """
        Initialize an AgentsClient instance.

        Configures the client to use the "agents" endpoint path and sets optional API key and server URL for authentication and server configuration. The initial state has no recorded agent response.

        Args:
            api_key: Optional API key for authenticating requests.
        """
        super().__init__(base_endpoint_path="agents", server_url=server_url, api_key=api_key, verbose=verbose)

    @staticmethod
    def agent_start_endpoint() -> NotteEndpoint[AgentResponse]:
        """
        Returns an endpoint for running an agent.

        Creates a NotteEndpoint configured with the AGENT_START path, a POST method, and an expected AgentResponse.
        """
        return NotteEndpoint(path=AgentsClient.AGENT_START, response=AgentResponse, method="POST")

    @staticmethod
    def agent_start_custom_endpoint() -> NotteEndpoint[AgentResponse]:
        """
        Returns an endpoint for running an agent.
        """
        return NotteEndpoint(path=AgentsClient.AGENT_START_CUSTOM, response=AgentResponse, method="POST")

    @staticmethod
    def agent_stop_endpoint(agent_id: str | None = None) -> NotteEndpoint[AgentResponse]:
        """
        Constructs a DELETE endpoint for stopping an agent.

        If an agent ID is provided, it is inserted into the endpoint URL. The returned
        endpoint is configured with the DELETE HTTP method and expects an AgentStatusResponse.

        Args:
            agent_id (str, optional): The identifier of the agent to stop. If omitted,
                the URL template will remain unformatted.

        Returns:
            NotteEndpoint[AgentResponse]: The endpoint object for stopping the agent.
        """
        path = AgentsClient.AGENT_STOP
        if agent_id is not None:
            path = path.format(agent_id=agent_id)
        return NotteEndpoint(path=path, response=AgentStatusResponse, method="DELETE")

    @staticmethod
    def agent_status_endpoint(agent_id: str | None = None) -> NotteEndpoint[AgentStatusResponse]:
        """
        Creates an endpoint for retrieving an agent's status.

        If an agent ID is provided, formats the endpoint path to target that specific agent.

        Args:
            agent_id: Optional identifier of the agent; if specified, the endpoint path will include this ID.

        Returns:
            NotteEndpoint configured with the GET method and AgentStatusResponse as the expected response.
        """
        path = AgentsClient.AGENT_STATUS
        if agent_id is not None:
            path = path.format(agent_id=agent_id)
        return NotteEndpoint(path=path, response=AgentStatusResponse, method="GET")

    @staticmethod
    def agent_replay_endpoint(agent_id: str | None = None) -> NotteEndpoint[BaseModel]:
        """
        Creates an endpoint for downloading an agent's replay.
        """
        path = AgentsClient.AGENT_REPLAY
        if agent_id is not None:
            path = path.format(agent_id=agent_id)
        return NotteEndpoint(path=path, response=BaseModel, method="GET")

    @staticmethod
    def agent_list_endpoint(params: AgentListRequest | None = None) -> NotteEndpoint[AgentResponse]:
        """
        Creates a NotteEndpoint for listing agents.

        Returns an endpoint configured with the agent listing path and a GET method.
        The optional params argument provides filtering or pagination details for the request.
        """
        return NotteEndpoint(
            path=AgentsClient.AGENT_LIST,
            response=AgentResponse,
            method="GET",
            request=None,
            params=params,
        )

    @override
    @staticmethod
    def endpoints() -> Sequence[NotteEndpoint[BaseModel]]:
        """
        Returns a list of endpoints for agent operations.

        Aggregates endpoints for running, stopping, checking status, and listing agents.
        """
        return [
            AgentsClient.agent_start_endpoint(),
            AgentsClient.agent_stop_endpoint(),
            AgentsClient.agent_status_endpoint(),
            AgentsClient.agent_list_endpoint(),
            AgentsClient.agent_replay_endpoint(),
        ]

    def start(self, **data: Unpack[AgentStartRequestDict]) -> AgentResponse:
        """
        Start an agent with the specified request parameters.

        Validates the provided data using the AgentRunRequest model, sends a run request through the
        designated endpoint, updates the last agent response, and returns the resulting AgentResponse.

        Args:
            **data: Keyword arguments representing the fields of an AgentRunRequest.

        Returns:
            AgentResponse: The response obtained from the agent run request.
        """
        request = AgentStartRequest.model_validate(data)
        response = self.request(AgentsClient.agent_start_endpoint().with_request(request))
        return response

    def wait(
        self,
        agent_id: str,
        polling_interval_seconds: int = 10,
        max_attempts: int = 30,
    ) -> AgentStatusResponse:
        """
        Waits for the specified agent to complete.

        Args:
            agent_id: The identifier of the agent to wait for.
            polling_interval_seconds: The interval between status checks.
            max_attempts: The maximum number of attempts to check the agent's status.

        Returns:
            AgentStatusResponse: The response from the agent status check.
        """
        last_step = 0
        for _ in range(max_attempts):
            response = self.status(agent_id=agent_id)
            if len(response.steps) > last_step:
                for step in response.steps[last_step:]:
                    step.log_pretty_string()
                    if step.is_done():
                        return response

                last_step = len(response.steps)

            if response.status == AgentStatus.closed:
                return response

            spinner = None
            try:
                if not WebpReplay.in_notebook():
                    spinner = Halo(
                        text=f"Waiting {polling_interval_seconds} seconds for agent to complete (current step: {last_step})...",
                    )
                time.sleep(polling_interval_seconds)

            finally:
                if spinner is not None:
                    _ = spinner.succeed()  #  pyright: ignore[reportUnknownMemberType]

        raise TimeoutError("Agent did not complete in time")

    async def watch_logs(self, agent_id: str, max_steps: int) -> AgentStatusResponse | None:
        """
        Watch the logs of the specified agent.
        """
        endpoint = NotteEndpoint(path=AgentsClient.AGENT_LOGS_WS, response=BaseModel, method="GET")
        wss_url = self.request_path(endpoint).format(agent_id=agent_id, token=self.token)
        wss_url = wss_url.replace("https://", "wss://").replace("http://", "ws://")

        async def get_messages() -> AgentStatusResponse | None:
            counter = 0
            async with websockets.client.connect(
                uri=wss_url,
                ping_interval=5,
                ping_timeout=40,
                close_timeout=5,
            ) as websocket:
                try:
                    async for message in websocket:
                        assert isinstance(message, str), f"Expected str, got {type(message)}"
                        try:
                            if agent_id in message and "agent_id" in message:
                                # termination condition
                                return AgentStatusResponse.model_validate_json(message)
                            response = AgentStepResponse.model_validate_json(message)
                            response.log_pretty_string()
                            counter += 1
                        except Exception as e:
                            if "error" in message:
                                logger.error(f"Error in agent logs: {message}")
                            elif agent_id in message and "agent_id" in message:
                                logger.error(f"Error parsing AgentStatusResponse for message: {message}: {e}")
                            else:
                                logger.error(f"Error parsing agent logs for message: {message}: {e}")
                            continue

                        if response.is_done():
                            logger.info(f"Agent {agent_id} completed in {counter} steps")
                            # wait for next AgentStatusResponse message
                            # break

                        if counter >= max_steps:
                            logger.info(f"Agent reached max steps: {max_steps}")
                            break
                except ConnectionError as e:
                    logger.error(f"Connection error: {e}")
                    return
                except Exception as e:
                    logger.error(f"Error: {e}")
                    return

        return await get_messages()

    async def watch_logs_and_wait(self, agent_id: str, max_steps: int) -> AgentStatusResponse:
        """
        Asynchronously execute a task with the agent.

        This is currently a wrapper around the synchronous run method.
        In future versions, this might be implemented as a true async operation.

        Args:
            task (str): The task description for the agent to execute.
            url (str | None): Optional starting URL for the task.

        Returns:
            AgentResponse: The response from the completed agent execution.
        """
        response = await self.watch_logs(agent_id=agent_id, max_steps=max_steps)
        if response is not None:
            return response
        # Wait max 9 seconds for the agent to complete
        TOTAL_WAIT_TIME, ITERATIONS = 9, 3
        for _ in range(ITERATIONS):
            time.sleep(TOTAL_WAIT_TIME / ITERATIONS)
            status = self.status(agent_id=agent_id)
            if status.status == AgentStatus.closed:
                return status
        time.sleep(TOTAL_WAIT_TIME)
        logger.error(f"[Agent] {agent_id} failed to complete in time. Try runnig `agent.status()` after a few seconds.")
        return self.status(agent_id=agent_id)

    def stop(self, agent_id: str) -> AgentResponse:
        """
        Stops the specified agent and clears the last agent response.

        Retrieves a valid agent identifier using the provided value or the last stored
        response, sends a stop request to the API, resets the internal agent response,
        and returns the resulting AgentResponse.

        Args:
            agent_id: The identifier of the agent to stop.

        Returns:
            AgentResponse: The response from the stop operation.

        Raises:
            ValueError: If a valid agent identifier cannot be determined.
        """
        endpoint = AgentsClient.agent_stop_endpoint(agent_id=agent_id)
        response = self.request(endpoint)
        return response

    def run(self, **data: Unpack[AgentStartRequestDict]) -> AgentStatusResponse:
        """
        Run an agent with the specified request parameters.
        and wait for completion

        Validates the provided data using the AgentCreateRequest model, sends a run request through the
        designated endpoint, updates the last agent response, and returns the resulting AgentResponse.
        """
        return asyncio.run(self.arun(**data))

    async def arun(self, **data: Unpack[AgentStartRequestDict]) -> AgentStatusResponse:
        """
        Run an async agent with the specified request parameters.
        and wait for completion

        Validates the provided data using the AgentCreateRequest model, sends a run request through the
        designated endpoint, updates the last agent response, and returns the resulting AgentResponse.
        """
        response = self.start(**data)
        # wait for completion
        max_steps: int = data.get("max_steps", DEFAULT_MAX_NB_STEPS)
        return await self.watch_logs_and_wait(agent_id=response.agent_id, max_steps=max_steps)

    def status(self, agent_id: str) -> AgentStatusResponse:
        """
        Retrieves the status of the specified agent.

        Queries the API for the current status of an agent using a validated agent ID.
        The provided ID is confirmed (or obtained from the last response if needed), and the
        resulting status is stored internally before being returned.

        Args:
            agent_id: Unique identifier of the agent to check.

        Returns:
            AgentResponse: The current status information of the specified agent.

        Raises:
            ValueError: If no valid agent ID can be determined.
        """
        request = AgentStatusRequest(agent_id=agent_id, replay=False)
        endpoint = AgentsClient.agent_status_endpoint(agent_id=agent_id).with_params(request)
        response = self.request(endpoint)
        return response

    def list(self, **data: Unpack[AgentListRequestDict]) -> Sequence[AgentResponse]:
        """
        Lists agents matching specified criteria.

        Validates the keyword arguments using the AgentListRequest model, constructs
        the corresponding endpoint for listing agents, and returns a sequence of agent
        responses.

        Args:
            data: Arbitrary keyword arguments representing filter criteria for agents.

        Returns:
            A sequence of AgentResponse objects.
        """
        params = AgentListRequest.model_validate(data)
        endpoint = AgentsClient.agent_list_endpoint(params=params)
        return self.request_list(endpoint)

    def replay(self, agent_id: str) -> WebpReplay:
        """
        Downloads the replay for the specified agent in webp format.

        Args:
            agent_id: The identifier of the agent to download the replay for.

        Returns:
            WebpReplay: The replay file in webp format.
        """
        endpoint = AgentsClient.agent_replay_endpoint(agent_id=agent_id)
        file_bytes = self._request_file(endpoint, file_type="webp")
        return WebpReplay(file_bytes)


class RemoteAgent:
    """
    A remote agent that can execute tasks through the Notte API.

    This class provides an interface for running tasks, checking status, and managing replays
    of agent executions. It maintains state about the current agent execution and provides
    methods to interact with the agent through an AgentsClient.

    Attributes:
        request (AgentCreateRequest): The configuration request used to create this agent.
        client (AgentsClient): The client used to communicate with the Notte API.
        response (AgentResponse | None): The latest response from the agent execution.
    """

    def __init__(
        self,
        client: AgentsClient,
        request: _AgentCreateRequest,
        headless: bool,
        open_viewer: Callable[[str], None],
        session: RemoteSession | None = None,
    ) -> None:
        """
        Initialize a new RemoteAgent instance.

        Args:
            client (AgentsClient): The client used to communicate with the Notte API.
            request (AgentCreateRequest): The configuration request for this agent.
        """
        self.headless: bool = headless
        self.open_viewer: Callable[[str], None] = open_viewer
        self.request: _AgentCreateRequest = request
        self.client: AgentsClient = client
        self.response: AgentResponse | None = None

    @property
    def agent_id(self) -> str:
        """
        Get the ID of the current agent execution.

        Returns:
            str: The unique identifier of the current agent execution.

        Raises:
            ValueError: If the agent hasn't been run yet (no response available).
        """
        if self.response is None:
            raise ValueError("You need to run the agent first to get the agent id")
        return self.response.agent_id

    def start(self, **data: Unpack[AgentStartRequestDict]) -> AgentResponse:
        """
        Start the agent with the specified request parameters.
        """
        self.response = self.client.start(**self.request.model_dump(), **data)
        if not self.headless:
            # start viewer
            self.open_viewer(self.response.session_id)
        return self.response

    def wait(self) -> AgentStatusResponse:
        """
        Wait for the agent to complete.
        """
        return self.client.wait(agent_id=self.agent_id)

    async def watch_logs(self) -> AgentStatusResponse | None:
        """
        Watch the logs of the agent.
        """
        return await self.client.watch_logs(agent_id=self.agent_id, max_steps=self.request.max_steps)

    async def watch_logs_and_wait(self) -> AgentStatusResponse:
        """
        Watch the logs of the agent and wait for completion.
        """
        return await self.client.watch_logs_and_wait(agent_id=self.agent_id, max_steps=self.request.max_steps)

    def stop(self) -> AgentResponse:
        """
        Stop the agent.
        """
        return self.client.stop(agent_id=self.agent_id)

    def run(self, **data: Unpack[AgentRunRequestDict]) -> AgentStatusResponse:
        """
        Execute a task with the agent.

        Runs the specified task and waits for its completion. If a URL is provided,
        the agent will start from that URL before executing the task.

        Args:
            task (str): The task description for the agent to execute.
            url (str | None): Optional starting URL for the task.

        Returns:
            AgentResponse: The response from the completed agent execution.
        """

        return asyncio.run(self.arun(**data))

    async def arun(self, **data: Unpack[AgentRunRequestDict]) -> AgentStatusResponse:
        """
        Asynchronously execute a task with the agent.

        This is currently a wrapper around the synchronous run method.
        In future versions, this might be implemented as a true async operation.

        Args:
            task (str): The task description for the agent to execute.
            url (str | None): Optional starting URL for the task.

        Returns:
            AgentResponse: The response from the completed agent execution.
        """
        self.response = self.start(**data)
        logger.info(f"[Agent] {self.agent_id} started with model: {self.request.reasoning_model}")
        return await self.watch_logs_and_wait()

    def run_custom(self, request: BaseModel) -> AgentStatusResponse:
        """
        Run an custom agent with the specified request parameters.
        and wait for completion

        Note: not all servers support custom agents.
        """
        if not self.client.is_custom_endpoint_available():
            raise ValueError(f"Custom endpoint is not available for this server: {self.client.server_url}")
        self.response = self.client.request(AgentsClient.agent_start_custom_endpoint().with_request(request))
        if not self.headless:
            # start viewer
            self.open_viewer(self.response.session_id)
        logger.info(f"[Custom Agent] {self.agent_id} started...")
        return asyncio.run(self.watch_logs_and_wait())

    def status(self) -> AgentStatusResponse:
        """
        Get the current status of the agent.

        Returns:
            AgentStatusResponse: The current status of the agent execution.

        Raises:
            ValueError: If the agent hasn't been run yet (no agent_id available).
        """
        return self.client.status(agent_id=self.agent_id)

    def replay(self) -> WebpReplay:
        """
        Get a replay of the agent's execution in WEBP format.

        Returns:
            WebpReplay: The replay data in WEBP format.

        Raises:
            ValueError: If the agent hasn't been run yet (no agent_id available).
        """
        return self.client.replay(agent_id=self.agent_id)


@final
class RemoteAgentFactory:
    """
    Factory for creating RemoteAgent instances.

    This factory provides a convenient way to create RemoteAgent instances with
    optional vault and session configurations. It handles the validation of
    agent creation requests and sets up the appropriate connections.

    Attributes:
        client (AgentsClient): The client used to communicate with the Notte API.
    """

    def __init__(self, client: AgentsClient, open_viewer: Callable[[str], None]) -> None:
        """
        Initialize a new RemoteAgentFactory instance.

        Args:
            client (AgentsClient): The client used to communicate with the Notte API.
        """
        self.client = client
        self.open_viewer = open_viewer

    def __call__(
        self,
        headless: bool = config.headless,
        vault: NotteVault | None = None,
        notifier: BaseNotifier | None = None,
        session: RemoteSession | None = None,
        raise_on_existing_contextual_session: bool = True,
        **data: Unpack[AgentCreateRequestDict],
    ) -> RemoteAgent:
        """
        Create a new RemoteAgent instance with the specified configuration.

        This method validates the agent creation request and sets up the appropriate
        connections with the provided vault and session if specified.

        Args:
            vault (NotteVault | None): Optional vault for secure credential storage.
            session (RemoteSessionFactory.RemoteSession | None): Optional session for persistent state.
            **data: Additional keyword arguments for the agent creation request.

        Returns:
            RemoteAgent: A new RemoteAgent instance configured with the specified parameters.
        """
        request = _AgentCreateRequest.model_validate(data)
        if notifier is not None:
            notifier_config = notifier.model_dump()
            request.notifier_config = notifier_config

        # #########################################################
        # ###################### Vault checks #####################
        # #########################################################

        if vault is not None:
            if len(vault.vault_id) == 0:
                raise ValueError("Vault ID cannot be empty")
            request.vault_id = vault.vault_id

        # #########################################################
        # #################### Session checks #####################
        # #########################################################

        if session is None:
            # check context var to provide better error message to users
            session_id = get_context_session_id()
            if session_id is not None:
                error_msg = (
                    f"[Session] {session_id} was found in the context but was not provided to the agent. "
                    "This is unexpected. If you meant to use this session inside the agent, use `notte.Agent(..., session=session)` instead."
                    " Otherwise, you can silence this error by setting `notte.Agent(..., raise_on_existing_contextual_session=False)`."
                )
                if raise_on_existing_contextual_session:
                    raise ValueError(error_msg)
                logger.warning(error_msg)

        if session is not None:
            if not isinstance(session, RemoteSession):  # pyright: ignore[reportUnnecessaryIsInstance]
                raise ValueError(
                    "You are trying to use a local session with a remote agent. This is not supported. Use `notte.Agent(session=session)` instead."
                )  # pyright: ignore[reportUnreachable]
            if len(session.session_id) == 0:
                raise ValueError("Session ID cannot be empty")
            request.session_id = session.session_id

            # headless check
            if session.headless != headless:
                logger.warning(
                    f"Session headless is {session.headless} but agent is headless={headless}. This is unexpected. Session flags will be prioritized over agent flags."
                )
                headless = session.headless

        return RemoteAgent(self.client, request, headless=headless, open_viewer=self.open_viewer)
