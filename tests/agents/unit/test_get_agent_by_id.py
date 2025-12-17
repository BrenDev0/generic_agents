import pytest 
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from src.shared.domain.exceptions.repositories import NotFoundException
from src.shared.domain.exceptions.permissions import PermissionsException
from src.agents.domain.entities import Agent
from src.agents.application.use_cases.get_agent_by_id import GetAgentById


@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
): 
    return GetAgentById(
        repository=mock_repository
    )


def test_success(
    mock_repository,
    use_case: GetAgentById
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

    result = use_case.execute(
        user_id=user_id,
        agent_id=agent_id
    )

    mock_repository.get_one.assert_called_once_with(
        key="agent_id",
        value=agent_id
    )

    assert result.agent_id == agent_id
    assert result.user_id == user_id

def test_not_found(
    mock_repository,
    use_case: GetAgentById
):
    
    agent_id = uuid4()
    user_id = uuid4()
    mock_repository.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        result = use_case.execute(
            user_id=user_id,
            agent_id=agent_id
        )

    assert "Agent not found" in str(exc_info)



def test_wrong_permissions(
    mock_repository,
    use_case: GetAgentById
):
    agent_id = uuid4()
    user_id = uuid4()

    not_my_agent = Agent(
        agent_id=agent_id,
        user_id=uuid4(),
        name="name",
        description="description",
        created_at=datetime.now()
    )

    mock_repository.get_one.return_value = not_my_agent

    with pytest.raises(PermissionsException) as exc_info:
        results = use_case.execute(
            user_id=user_id,
            agent_id=agent_id
        )

    
    assert "Forbidden" in str(exc_info)

