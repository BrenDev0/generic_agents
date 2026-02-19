import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import Mock
from src.features.messages.application.use_cases.create import CreateMessage
from src.features.messages.domain import CreateMessageRequest, Message


@pytest.fixture
def mock_message_repository():
    return Mock()

@pytest.fixture
def mock_message_service():
    return Mock()

@pytest.fixture
def use_case(mock_message_repository, mock_message_service):
    return CreateMessage(
        message_repository=mock_message_repository,
        message_service=mock_message_service
    )

@pytest.fixture
def chat_id():
    return uuid4()

@pytest.fixture
def create_request(chat_id):
    return CreateMessageRequest(
        chat_id=chat_id,
        type="user",
        text="Test message content"
    )

@pytest.fixture
def mock_partial_entity():
    return Mock(spec=Message)

@pytest.fixture
def mock_created_message(chat_id):
    message = Mock(spec=Message)
    message.message_id = uuid4()
    message.chat_id = chat_id
    message.type = "user"
    message.text = "Test message content"
    message.created_at = datetime.now()
    return message

@pytest.fixture
def mock_decrypted_message(chat_id):
    message = Mock(spec=Message)
    message.message_id = uuid4()
    message.chat_id = chat_id
    message.type = "user"
    message.text = "Test message content"
    message.created_at = datetime.now()
    return message


def test_execute_success(
    use_case,
    mock_message_repository,
    mock_message_service,
    create_request,
    mock_partial_entity,
    mock_created_message,
    mock_decrypted_message
):
    # Arrange
    mock_message_service.prepare_new_message_data.return_value = mock_partial_entity
    mock_message_repository.create.return_value = mock_created_message
    mock_message_service.get_decrypted_entity.return_value = mock_decrypted_message
    
    # Act
    result = use_case.execute(data=create_request)
    
    # Assert
    mock_message_service.prepare_new_message_data.assert_called_once_with(data=create_request)
    mock_message_repository.create.assert_called_once_with(data=mock_partial_entity)
    mock_message_service.get_decrypted_entity.assert_called_once_with(mock_created_message)
    assert result == mock_decrypted_message


def test_execute_calls_service_to_prepare_data(
    use_case,
    mock_message_service,
    mock_message_repository,
    create_request,
    mock_partial_entity,
    mock_created_message
):
    # Arrange
    mock_message_service.prepare_new_message_data.return_value = mock_partial_entity
    mock_message_repository.create.return_value = mock_created_message
    mock_message_service.get_decrypted_entity.return_value = Mock()
    
    # Act
    use_case.execute(data=create_request)
    
    # Assert
    mock_message_service.prepare_new_message_data.assert_called_once()
    call_args = mock_message_service.prepare_new_message_data.call_args
    assert call_args.kwargs["data"] == create_request


def test_execute_passes_prepared_data_to_repository(
    use_case,
    mock_message_service,
    mock_message_repository,
    create_request,
    mock_partial_entity,
    mock_created_message
):
    # Arrange
    mock_message_service.prepare_new_message_data.return_value = mock_partial_entity
    mock_message_repository.create.return_value = mock_created_message
    mock_message_service.get_decrypted_entity.return_value = Mock()
    
    # Act
    use_case.execute(data=create_request)
    
    # Assert
    mock_message_repository.create.assert_called_once_with(data=mock_partial_entity)


def test_execute_decrypts_created_message(
    use_case,
    mock_message_service,
    mock_message_repository,
    create_request,
    mock_partial_entity,
    mock_created_message
):
    # Arrange
    mock_message_service.prepare_new_message_data.return_value = mock_partial_entity
    mock_message_repository.create.return_value = mock_created_message
    mock_message_service.get_decrypted_entity.return_value = Mock()
    
    # Act
    use_case.execute(data=create_request)
    
    # Assert
    mock_message_service.get_decrypted_entity.assert_called_once_with(mock_created_message)


def test_execute_returns_decrypted_entity(
    use_case,
    mock_message_service,
    mock_message_repository,
    create_request,
    mock_partial_entity,
    mock_created_message,
    mock_decrypted_message
):
    # Arrange
    mock_message_service.prepare_new_message_data.return_value = mock_partial_entity
    mock_message_repository.create.return_value = mock_created_message
    mock_message_service.get_decrypted_entity.return_value = mock_decrypted_message
    
    # Act
    result = use_case.execute(data=create_request)
    
    # Assert
    assert result == mock_decrypted_message


def test_execute_preserves_message_content(
    use_case,
    mock_message_service,
    mock_message_repository,
    chat_id
):
    # Arrange
    test_text = "Important message"
    create_request = CreateMessageRequest(
        chat_id=chat_id,
        type="assistant",
        text=test_text
    )
    mock_message_service.prepare_new_message_data.return_value = Mock()
    mock_message_repository.create.return_value = Mock()
    mock_decrypted_message = Mock(spec=Message)
    mock_decrypted_message.text = test_text
    mock_decrypted_message.type = "assistant"
    mock_message_service.get_decrypted_entity.return_value = mock_decrypted_message
    
    # Act
    result = use_case.execute(data=create_request)
    
    # Assert
    assert result.text == test_text
    assert result.type == "assistant"