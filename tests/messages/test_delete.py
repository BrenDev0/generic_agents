import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import Mock
from src.features.messages.application.use_cases.delete import DeleteMessages
from src.features.messages.domain import Message, MessagePublic


@pytest.fixture
def mock_message_repository():
    return Mock()

@pytest.fixture
def mock_message_service():
    return Mock()

@pytest.fixture
def use_case(mock_message_repository, mock_message_service):
    return DeleteMessages(
        message_repository=mock_message_repository,
        message_service=mock_message_service
    )

@pytest.fixture
def chat_id():
    return uuid4()

@pytest.fixture
def message_ids():
    return [uuid4(), uuid4(), uuid4()]

@pytest.fixture
def mock_deleted_messages(chat_id, message_ids):
    messages = []
    for msg_id in message_ids:
        message = Mock(spec=Message)
        message.message_id = msg_id
        message.chat_id = chat_id
        message.type = "user"
        message.text = f"Message {msg_id}"
        message.created_at = datetime.now()
        messages.append(message)
    return messages

@pytest.fixture
def mock_public_messages(chat_id, message_ids):
    return [
        MessagePublic(
            message_id=msg_id,
            chat_id=chat_id,
            type="user",
            text=f"Message {msg_id}",
            created_at=datetime.now()
        )
        for msg_id in message_ids
    ]


def test_execute_success_deletes_multiple_messages(
    use_case,
    mock_message_repository,
    mock_message_service,
    message_ids,
    mock_deleted_messages,
    mock_public_messages
):
    mock_message_repository.delete_many.return_value = mock_deleted_messages
    mock_message_service.get_public_schema.side_effect = mock_public_messages
    
    result = use_case.execute(message_ids=message_ids)
    
    mock_message_repository.delete_many.assert_called_once_with(
        key="message_id",
        value=message_ids
    )
    assert len(result) == len(message_ids)
    assert result == mock_public_messages


def test_execute_empty_list_when_no_messages_deleted(
    use_case,
    mock_message_repository,
    mock_message_service,
    message_ids
):
    mock_message_repository.delete_many.return_value = []
    
    result = use_case.execute(message_ids=message_ids)
    
    mock_message_repository.delete_many.assert_called_once()
    mock_message_service.get_public_schema.assert_not_called()
    assert result == []


def test_execute_calls_repository_with_correct_params(
    use_case,
    mock_message_repository,
    mock_message_service,
    message_ids
):
    mock_message_repository.delete_many.return_value = []
    
    use_case.execute(message_ids=message_ids)
    
    call_args = mock_message_repository.delete_many.call_args
    assert call_args.kwargs["key"] == "message_id"
    assert call_args.kwargs["value"] == message_ids


def test_execute_transforms_all_deleted_messages(
    use_case,
    mock_message_repository,
    mock_message_service,
    message_ids,
    mock_deleted_messages,
    mock_public_messages
):
    mock_message_repository.delete_many.return_value = mock_deleted_messages
    mock_message_service.get_public_schema.side_effect = mock_public_messages
    
    use_case.execute(message_ids=message_ids)
    
    assert mock_message_service.get_public_schema.call_count == len(mock_deleted_messages)
    for message in mock_deleted_messages:
        mock_message_service.get_public_schema.assert_any_call(message)


def test_execute_returns_list_of_public_schemas(
    use_case,
    mock_message_repository,
    mock_message_service,
    message_ids,
    mock_deleted_messages,
    mock_public_messages
):
    mock_message_repository.delete_many.return_value = mock_deleted_messages
    mock_message_service.get_public_schema.side_effect = mock_public_messages
    
    result = use_case.execute(message_ids=message_ids)
    
    assert isinstance(result, list)
    assert all(isinstance(msg, MessagePublic) for msg in result)


def test_execute_with_single_message(
    use_case,
    mock_message_repository,
    mock_message_service,
    chat_id
):
    single_id = uuid4()
    deleted_message = Mock(spec=Message)
    deleted_message.message_id = single_id
    public_message = MessagePublic(
        message_id=single_id,
        chat_id=chat_id,
        type="user",
        text="Single message",
        created_at=datetime.now()
    )
    
    mock_message_repository.delete_many.return_value = [deleted_message]
    mock_message_service.get_public_schema.return_value = public_message
    
    result = use_case.execute(message_ids=[single_id])
    
    assert len(result) == 1
    assert result[0] == public_message
