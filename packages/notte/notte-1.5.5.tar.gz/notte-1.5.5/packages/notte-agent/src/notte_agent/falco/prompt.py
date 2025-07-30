import datetime as dt
import json
from collections.abc import Sequence
from enum import StrEnum
from pathlib import Path

import chevron
from notte_core.actions import (
    BaseAction,
    ClickAction,
    CompletionAction,
    FillAction,
    GotoAction,
    ScrapeAction,
)
from notte_core.errors.processing import InvalidInternalCheckError

system_prompt_dir = Path(__file__).parent / "prompts"


class ActionRegistry:
    """Union of all possible actions"""

    @staticmethod
    def render() -> str:
        """Returns a markdown formatted description of all available actions."""
        descriptions: list[str] = []

        for action_name, action_cls in BaseAction.ACTION_REGISTRY.items():
            try:
                # Get schema and safely remove common fields
                skip_keys = action_cls.non_agent_fields().difference(set(["description"]))
                sub_skip_keys = ["title", "$ref"]
                schema = {
                    k: {sub_k: sub_v for sub_k, sub_v in v.items() if sub_k not in sub_skip_keys}
                    for k, v in action_cls.model_json_schema()["properties"].items()
                    if k not in skip_keys
                }
                # schema['id'] = schema['id']['default']
                __description: dict[str, str] = schema.pop("description", "No description available")  # type: ignore[type-arg]
                if "default" not in __description:
                    raise InvalidInternalCheckError(
                        check=f"description should have a default value for {action_cls.__name__}",
                        url="unknown url",
                        dev_advice="This should never happen.",
                    )
                _description: str = __description["default"]
                # Format as: ActionName: {param1: {type: str, description: ...}, ...}
                description = f"""
* "{action_name}" : {_description}. Format:
```json
{json.dumps(schema)}
```
"""
                descriptions.append(description)
            except Exception as e:
                descriptions.append(f"Error getting schema for {action_cls.__name__}: {str(e)}")

        return "".join(descriptions)


class PromptType(StrEnum):
    SINGLE_ACTION = "single_action"
    MULTI_ACTION = "multi_action"

    def prompt_file(self) -> Path:
        match self:
            case PromptType.SINGLE_ACTION:
                return system_prompt_dir / "system_prompt_single_action.md"
            case PromptType.MULTI_ACTION:
                return system_prompt_dir / "system_prompt_multi_action.md"


class FalcoPrompt:
    def __init__(
        self,
        max_actions_per_step: int,
    ) -> None:
        multi_act = max_actions_per_step > 1
        prompt_type = PromptType.MULTI_ACTION if multi_act else PromptType.SINGLE_ACTION
        self.system_prompt: str = prompt_type.prompt_file().read_text()
        self.max_actions_per_step: int = max_actions_per_step

    @staticmethod
    def action_registry() -> str:
        return ActionRegistry.render()

    @staticmethod
    def _json_dump(actions: Sequence[BaseAction]) -> str:
        lines = ",\n  ".join([action.model_dump_agent_json() for action in actions])
        return "[\n  " + lines + "\n]"

    def example_form_filling(self) -> str:
        return self._json_dump(
            actions=[
                FillAction(id="I99", value="username"),
                FillAction(id="I101", value="password"),
                ClickAction(id="B1"),
            ]
        )

    def example_invalid_sequence(self) -> str:
        return self._json_dump(actions=[ClickAction(id="L1"), ClickAction(id="B4"), ClickAction(id="L2")])

    def example_navigation_and_extraction(self) -> str:
        return self._json_dump(
            [GotoAction(url="https://www.google.com"), ScrapeAction(instructions="Extract the search results")]
        )

    def completion_example(self) -> str:
        return self._json_dump([CompletionAction(success=True, answer="<answer to the task>")])

    def example_step(self) -> str:
        goal_eval = (
            "Analyze the current elements and the image to check if the previous goals/actions"
            " are successful like intended by the task. Ignore the action result. The website is the ground truth. "
            "Also mention if something unexpected happened like new suggestions in an input field. "
            "Shortly state why/why not"
        )
        return chevron.render(
            """
{
  "state": {
    "page_summary": "On the page are company a,b,c wtih their revenue 1,2,3.",
    "relevant_interactions": [{"id": "B2", "reason": "The button with id B2 represents search and I'm looking to search"}],
    "previous_goal_status": "success|failure|unknown",
    "previous_goal_eval": "{{goal_eval}}",
    "memory": "Description of what has been done and what you need to remember until the end of the task",
    "next_goal": "What needs to be done with the next actions"
  },
  "actions": [
   {
      "type: "one_action_type",
      // action-specific parameter
      ...
   }, // ... more actions in sequence ...
  ]
}
""",
            {"goal_eval": goal_eval},
        )

    def system(self) -> str:
        return chevron.render(
            self.system_prompt,
            {
                "timstamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "max_actions_per_step": self.max_actions_per_step,
                "action_description": self.action_registry(),
                "example_form_filling": self.example_form_filling(),
                "example_step": self.example_step(),
                "completion_example": self.completion_example(),
                "completion_action_name": CompletionAction.name(),
                "goto_action_name": GotoAction.name(),
                "example_navigation_and_extraction": self.example_navigation_and_extraction(),
                "example_invalid_sequence": self.example_invalid_sequence(),
            },
        )

    def task(self, task: str):
        return f"""
Your ultimate task is: "{task}".
If you achieved your ultimate task, stop everything and use the done action in the next step to complete the task.
If not, continue as usual.
"""

    def new_task(self, task: str) -> str:
        return f"""
Your new ultimate task is: {task}.
Take the previous context into account and finish your new ultimate task.
"""

    def action_message(self) -> str:
        return """Given the previous information, start by reflecting on your last action. Then, summarize the current page and list relevant available interactions.
Absolutely do not under any circumstance list or pay attention to any id that is not explicitly found in the page.
From there, select the your next goal, and in turn, your next action.
    """
