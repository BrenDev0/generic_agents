import pytest
from unittest.mock import Mock
from uuid import uuid4
from src.features.chats.application.use_cases.create import CreateChat
from src.features.chats.domain.entities import Chat
from datetime import datetime

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
):
    return CreateChat(
        chat_repository=mock_repository
    )


def test_success(
    mock_repository,
    use_case: CreateChat
):  
    chat_id = uuid4()
    agent_id = uuid4()
    fake_chat = Chat(
        chat_id=chat_id,
        agent_id=agent_id,
        created_at=datetime.now()
    )

    mock_repository.create.return_value = fake_chat

    result = use_case.execute(
        chat_id=chat_id,
        agent_id=agent_id
    )

    mock_repository.create.assert_called_once()
    assert result.agent_id == agent_id
    