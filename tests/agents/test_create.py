import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import Mock
from src.features.agents.application.use_cases.create import CreateAgentProfile
from src.features.agents.domain.entities import Agent
from src.features.agents.domain.schemas import CreateAgentProfileRequest

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
):
    return CreateAgentProfile(
        repository=mock_repository
    )

def test_create_agent_success(
    mock_repository,
    use_case: CreateAgentProfile
):
    user_id = uuid4()
    fake_agent = Agent(
        agent_id=uuid4(),
        user_id=user_id,
        name="test_name",
        description="test_description", 
        agent_state=True,
        created_at=datetime.now()
    )

    req = CreateAgentProfileRequest(
        name="test_name",
        description="test_description"
    )
    mock_repository.create.return_value = fake_agent

    result = use_case.execute(
        user_id=user_id,
        profile=req
    )

    assert result.user_id == user_id