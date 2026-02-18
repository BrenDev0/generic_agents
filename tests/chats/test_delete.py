import pytest 
from unittest.mock import Mock
from datetime import datetime
from uuid import uuid4
from src.features.chats.application.use_cases.delete import DeleteChat
from src.features.chats.domain.entities import Chat
from src.features.agents.domain.entities import Agent
from src.persistence import NotFoundException
from src.security import PermissionsException

@pytest.fixture
def mock_chat_repository():
    return Mock()

@pytest.fixture
def use_case(mock_chat_repository):
    return DeleteChat(
        chat_repository=mock_chat_repository
    )


def test_success(
    mock_chat_repository,
    use_case: DeleteChat
):
    chat_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()

    fake_agent = Agent(
        agent_id=agent_id,
        user_id=user_id,
        name="test",
        description="test",
        agent_state=True,
        created_at=datetime.now()
    )
    fake_chat = Chat(
        chat_id=chat_id,
        agent_id=agent_id,
        created_at=datetime.now(),
        agent=fake_agent
    )

    mock_chat_repository.get_one.return_value = fake_chat
    mock_chat_repository.delete.return_value = fake_chat

    result = use_case.execute(
        user_id=user_id,
        chat_id=chat_id
    )

    assert result.chat_id == chat_id



def test_not_found(
    mock_chat_repository,
    use_case: DeleteChat
):
    chat_id = uuid4()
    user_id = uuid4()

    mock_chat_repository.get_one.return_value = None
   
    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            user_id=user_id,
            chat_id=chat_id
        )

    mock_chat_repository.delete.assert_not_called()
    assert "404" in str(exc_info)
    

def test_permissions_error(
    mock_chat_repository,
    use_case: DeleteChat
):
    chat_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()

    fake_agent = Agent(
        agent_id=agent_id,
        user_id=uuid4(),
        name="test",
        description="test",
        agent_state=True,
        created_at=datetime.now()
    )
    fake_chat = Chat(
        chat_id=chat_id,
        agent_id=agent_id,
        created_at=datetime.now(),
        agent=fake_agent
    )

    mock_chat_repository.get_one.return_value = fake_chat

    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            chat_id=chat_id
        )

    mock_chat_repository.delete.assert_not_called()
    assert "403" in str(exc_info)

    