import pytest
from uuid import uuid4
from unittest.mock import Mock
from datetime import datetime
from src.agents.application.use_cases.update import UpdateAgentProfile
from src.agents.domain.entities import Agent
from src.shared.domain.exceptions.permissions import PermissionsException
from src.shared.domain.exceptions.repositories import NotFoundException
from src.agents.domain.schemas import AgentPublic, UpdatAgentProfileRequest

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
): 
    return UpdateAgentProfile(
        repository=mock_repository
    )


def test_success(
    mock_repository,
    use_case: UpdateAgentProfile
):
    agent_id = uuid4()
    user_id = uuid4()

    changes = UpdatAgentProfileRequest(
        name="updated_name",
        description="updated_description"
    )

    fake_agent = Agent(
        agent_id=agent_id,
        user_id=user_id,
        name="name",
        description="description",
        created_at=datetime.now()
    )

    fake_updated_agent = Agent(
        agent_id=agent_id,
        user_id=user_id,
        name="updated_name",
        description="updated_description",
        created_at=datetime.now()
    )

    mock_repository.get_one.return_value = fake_agent
    mock_repository.update.return_value = fake_updated_agent

    result = use_case.execute(
        user_id=user_id,
        agent_id=agent_id,
        changes=changes
    )

    mock_repository.get_one.assert_called_once_with(
        key="agent_id",
        value=agent_id
    )

    mock_repository.update.assert_called_once_with(
        key="agent_id",
        value=agent_id,
        changes=changes.model_dump()
    )

    assert result.name == "updated_name"
    assert isinstance(result, AgentPublic)




