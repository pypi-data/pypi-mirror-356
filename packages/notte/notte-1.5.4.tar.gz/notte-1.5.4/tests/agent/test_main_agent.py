import pytest
from notte_agent.main import Agent, AgentType
from pydantic import ValidationError


@pytest.fixture
def task():
    return "go to notte.cc and extract the pricing plans"


def test_falco_agent(task: str):
    agent = Agent(agent_type=AgentType.FALCO, max_steps=5)
    assert agent is not None
    response = agent.run(task=task)
    assert response is not None
    assert response.success
    assert response.answer is not None
    assert response.answer != ""


@pytest.mark.skip("Renable that later on when we fix the gufo agent")
def test_gufo_agent(task: str):
    agent = Agent(agent_type=AgentType.GUFO, max_steps=5)
    assert agent is not None
    response = agent.run(task=task)
    assert response is not None
    assert response.success
    assert response.answer is not None
    assert response.answer != ""


def test_falco_agent_external_model(task: str):
    agent = Agent(agent_type=AgentType.FALCO, max_steps=1, reasoning_model="gemini/gemini-2.5-flash-preview-05-20")
    assert agent is not None
    response = agent.run(task=task)
    assert response is not None
    assert response.answer is not None
    assert response.answer != ""


def test_falco_agent_invalid_external_model_should_fail(task: str):
    with pytest.raises(ValidationError):
        agent = Agent(agent_type=AgentType.FALCO, max_steps=2, reasoning_model="notavalid/gpt-4o-mini")
        _ = agent.run(task=task)
