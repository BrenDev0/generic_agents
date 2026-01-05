import pytest 
from uuid import uuid4
from datetime import datetime
from unittest.mock import Mock
from src.features.agents.application.use_cases.collection import GetAgentsByUser
from src.features.agents.domain.entities import Agent

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
):
    return GetAgentsByUser(repository=mock_repository)


def test_success(
    mock_repository,
    use_case: GetAgentsByUser
):
    user_id = uuid4()
    mock_collection = [
        Agent(
            agent_id=uuid4(),
            user_id=user_id,
            name="agent_1",
            description="...",
            created_at=datetime.now()
        ),
        Agent(
            agent_id=uuid4(),
            user_id=user_id,
            name="agent_2",
            description="...",
            created_at=datetime.now()
        )
    ]

    mock_repository.get_many.return_value = mock_collection

    result = use_case.execute(
        user_id=user_id
    )

    mock_repository.get_many.assert_called_once_with(
        key="user_id",
        value=user_id
    )
    assert isinstance(result, list)
    assert len(result) == 2

def test_no_results(
    mock_repository,
    use_case: GetAgentsByUser
):
    user_id = uuid4()
    mock_repository.get_many.return_value = None

    result = use_case.execute(
        user_id=user_id
    )

    assert isinstance(result, list)
    assert len(result) == 0