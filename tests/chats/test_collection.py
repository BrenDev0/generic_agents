import pytest 
from uuid import uuid4
from datetime import datetime
from unittest.mock import Mock
from src.security import PermissionsException
from src.features.chats.application.use_cases.collection import GetChatsCollection
from src.features.chats.domain.entities import Chat
from src.features.agents.domain.entities import Agent

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
):
    return GetChatsCollection(chat_repository=mock_repository)


def test_success(
    mock_repository,
    use_case: GetChatsCollection
):
    user_id = uuid4()
    agent_id = uuid4()
    fake_agent = Agent(
        agent_id=agent_id,
        user_id=user_id,
        name="agent_1",
        description="...",
        agent_state=True,
        created_at=datetime.now()
    )
    mock_collection = [
        Chat(
            chat_id=uuid4(),
            agent_id=agent_id,
            created_at=datetime.now(),
            agent=fake_agent
        ),
        Chat(
            chat_id=uuid4(),
            agent_id=agent_id,
            created_at=datetime.now(),
            agent=fake_agent
        )
    ]

    mock_repository.get_many.return_value = mock_collection

    result = use_case.execute(
        user_id=user_id,
        agent_id=agent_id,
        page_number=2,
        per_page=20
    )

    mock_repository.get_many.assert_called_once_with(
        key="agent_id",
        value=agent_id,
        limit=20,
        offset=20
    )
    assert isinstance(result, list)
    assert len(result) == 2

def test_no_results(
    mock_repository,
    use_case: GetChatsCollection
):
    user_id = uuid4()
    agent_id = uuid4()
    mock_repository.get_many.return_value = None

    result = use_case.execute(
        user_id=user_id,
        agent_id=agent_id,
        page_number=1,
        per_page=20
    )

    assert isinstance(result, list)
    assert len(result) == 0


def test_permissions_error(
    mock_repository,
    use_case: GetChatsCollection
):
    user_id = uuid4()
    agent_id = uuid4()
    fake_agent = Agent(
        agent_id=agent_id,
        user_id=uuid4(),
        name="agent_1",
        description="...",
        agent_state=True,
        created_at=datetime.now()
    )
    mock_collection = [
        Chat(
            chat_id=uuid4(),
            agent_id=agent_id,
            created_at=datetime.now(),
            agent=fake_agent
        ),
        Chat(
            chat_id=uuid4(),
            agent_id=agent_id,
            created_at=datetime.now(),
            agent=fake_agent
        )
    ]

    mock_repository.get_many.return_value = mock_collection

    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            agent_id=agent_id,
            page_number=2,
            per_page=20
        )

    mock_repository.get_many.assert_called_once_with(
        key="agent_id",
        value=agent_id,
        limit=20,
        offset=20
    )
    
    assert "403" in str(exc_info)