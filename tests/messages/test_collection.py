import pytest
from uuid import uuid4
from unittest.mock import Mock
from src.features.messages.application.use_cases.collection import GetMessageCollection
from src.features.messages.domain import Message


class TestGetMessageCollection:
    
    @pytest.fixture
    def mock_message_repository(self):
        return Mock()
    
    @pytest.fixture
    def mock_message_service(self):
        return Mock()
    
    @pytest.fixture
    def use_case(self, mock_message_repository, mock_message_service):
        return GetMessageCollection(
            message_repository=mock_message_repository,
            message_service=mock_message_service
        )
    
    @pytest.fixture
    def chat_id(self):
        return uuid4()
    
    @pytest.fixture
    def mock_messages(self):
        return [Mock(spec=Message), Mock(spec=Message), Mock(spec=Message)]
    
    @pytest.fixture
    def mock_public_messages(self):
        return [
            {"id": "1", "content": "Message 1"},
            {"id": "2", "content": "Message 2"},
            {"id": "3", "content": "Message 3"}
        ]
    
    def test_execute_success_with_messages(
        self, 
        use_case, 
        mock_message_repository, 
        mock_message_service,
        mock_messages,
        mock_public_messages,
        chat_id
    ):
        # Arrange
        page_number = 1
        per_page = 10
        mock_message_repository.get_many.return_value = mock_messages
        mock_message_service.get_public_schema.side_effect = mock_public_messages
        
        # Act
        result = use_case.execute(chat_id=chat_id, page_number=page_number, per_page=per_page)
        
        # Assert
        mock_message_repository.get_many.assert_called_once_with(
            key="chat_id",
            value=chat_id,
            limit=per_page,
            offset=0
        )
        assert mock_message_service.get_public_schema.call_count == len(mock_messages)
        assert result == mock_public_messages
    
    def test_execute_empty_result(
        self,
        use_case,
        mock_message_repository,
        mock_message_service,
        chat_id
    ):
        # Arrange
        page_number = 1
        per_page = 10
        mock_message_repository.get_many.return_value = None
        
        # Act
        result = use_case.execute(chat_id=chat_id, page_number=page_number, per_page=per_page)
        
        # Assert
        mock_message_repository.get_many.assert_called_once()
        mock_message_service.get_public_schema.assert_not_called()
        assert result == []
    
    def test_execute_calculates_offset_correctly_page_2(
        self,
        use_case,
        mock_message_repository,
        mock_message_service,
        chat_id
    ):
        # Arrange
        page_number = 2
        per_page = 10
        expected_offset = 10
        mock_message_repository.get_many.return_value = []
        
        # Act
        use_case.execute(chat_id=chat_id, page_number=page_number, per_page=per_page)
        
        # Assert
        mock_message_repository.get_many.assert_called_once_with(
            key="chat_id",
            value=chat_id,
            limit=per_page,
            offset=expected_offset
        )
    
    def test_execute_calculates_offset_correctly_page_5(
        self,
        use_case,
        mock_message_repository,
        mock_message_service,
        chat_id
    ):
        # Arrange
        page_number = 5
        per_page = 20
        expected_offset = 80  # (5-1) * 20
        mock_message_repository.get_many.return_value = []
        
        # Act
        use_case.execute(chat_id=chat_id, page_number=page_number, per_page=per_page)
        
        # Assert
        mock_message_repository.get_many.assert_called_once_with(
            key="chat_id",
            value=chat_id,
            limit=per_page,
            offset=expected_offset
        )
    
    def test_execute_transforms_all_messages(
        self,
        use_case,
        mock_message_repository,
        mock_message_service,
        mock_messages,
        chat_id
    ):
        # Arrange
        page_number = 1
        per_page = 10
        mock_message_repository.get_many.return_value = mock_messages
        mock_message_service.get_public_schema.return_value = {"transformed": True}
        
        # Act
        result = use_case.execute(chat_id=chat_id, page_number=page_number, per_page=per_page)
        
        # Assert
        assert len(result) == len(mock_messages)
        for message in mock_messages:
            mock_message_service.get_public_schema.assert_any_call(message)