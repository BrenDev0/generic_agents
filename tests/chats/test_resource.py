import pytest
from uuid import uuid4
from unittest.mock import Mock, MagicMock
from src.features.chats.application.use_cases.resource import GetChatResource
from src.features.chats.domain import Chat
from src.persistence import NotFoundException
from src.security import PermissionsException


class TestGetChatResource:
    
    @pytest.fixture
    def mock_chat_repository(self):
        return Mock()
    
    @pytest.fixture
    def use_case(self, mock_chat_repository):
        return GetChatResource(chat_repository=mock_chat_repository)
    
    @pytest.fixture
    def user_id(self):
        return uuid4()
    
    @pytest.fixture
    def chat_id(self):
        return uuid4()
    
    @pytest.fixture
    def mock_chat(self, user_id):
        chat = Mock(spec=Chat)
        chat.agent = MagicMock()
        chat.agent.user_id = user_id
        return chat
    
    def test_execute_success(self, use_case, mock_chat_repository, mock_chat, user_id, chat_id):
        mock_chat_repository.get_one.return_value = mock_chat
    
        result = use_case.execute(user_id=user_id, chat_id=chat_id)
        
        mock_chat_repository.get_one.assert_called_once_with(
            key="chat_id",
            value=chat_id
        )
        assert result == mock_chat
    
    def test_execute_chat_not_found(self, use_case, mock_chat_repository, user_id, chat_id):
        mock_chat_repository.get_one.return_value = None
        
        with pytest.raises(NotFoundException):
            use_case.execute(user_id=user_id, chat_id=chat_id)
    
    def test_execute_permission_denied(self, use_case, mock_chat_repository, mock_chat, chat_id):
        different_user_id = uuid4()
        mock_chat_repository.get_one.return_value = mock_chat
        
        with pytest.raises(PermissionsException):
            use_case.execute(user_id=different_user_id, chat_id=chat_id)
    
    def test_execute_calls_repository_with_correct_params(self, use_case, mock_chat_repository, mock_chat, user_id, chat_id):
        mock_chat_repository.get_one.return_value = mock_chat
        
        use_case.execute(user_id=user_id, chat_id=chat_id)
        
        mock_chat_repository.get_one.assert_called_once()
        call_args = mock_chat_repository.get_one.call_args
        assert call_args.kwargs["key"] == "chat_id"
        assert call_args.kwargs["value"] == chat_id