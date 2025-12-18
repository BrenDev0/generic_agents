import pytest
from uuid import uuid4
from unittest.mock import Mock
from datetime import datetime
from src.shared.domain.exceptions.repositories import NotFoundException
from src.shared.domain.exceptions.permissions import PermissionsException
from src.agents.application.use_cases.delete import DeleteAgentProfile
from src.agents.domain.entities import Agent

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
):
    return DeleteAgentProfile(repository=mock_repository)


def test_success(
    mock_repository,
    use_case: DeleteAgentProfile
):
    agent_id = uuid4()
    user_id = uuid4()

    fake_agent = Agent(
        agent_id=agent_id,
        user_id=user_id,
        name="name",
        description="description",
        created_at=datetime.now()
    )

    mock_repository.get_one.return_value = fake_agent

    mock_repository.delete.return_value = fake_agent

    result = use_case.execute(
        user_id=user_id,
        agent_id=agent_id
    )

    mock_repository.get_one.assert_called_once_with(
        key="agent_id",
        value=agent_id
    )

    mock_repository.delete.assert_called_once_with(
        key="agent_id",
        value=fake_agent.agent_id
    )
    assert result.user_id == user_id
    assert result.agent_id == agent_id


def test_not_found(
    mock_repository,
    use_case: DeleteAgentProfile
):
    user_id = uuid4()
    agent_id = uuid4()


    mock_repository.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        result = use_case.execute(
            user_id=user_id,
            agent_id=agent_id
        )

    mock_repository.get_one.assert_called_once_with(
        key="agent_id",
        value=agent_id
    )

    mock_repository.delete.assert_not_called()
    assert "Agent not found" in str(exc_info)


def test_permission_error(
    mock_repository,
    use_case: DeleteAgentProfile
):
    user_id = uuid4()
    agent_id = uuid4()

    fake_agent = Agent(
        agent_id=agent_id,
        user_id=uuid4(),
        name="name",
        description="description",
        created_at=datetime.now()
    )

    mock_repository.get_one.return_value = fake_agent

    with pytest.raises(PermissionsException) as exc_info:
        result = use_case.execute(
            user_id=user_id,
            agent_id=agent_id
        )

    mock_repository.get_one.assert_called_once_with(
        key="agent_id",
        value=agent_id
    )

    mock_repository.delete.assert_not_called()
    assert "Forbidden" in str(exc_info)
