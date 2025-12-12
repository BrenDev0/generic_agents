import pytest
from uuid import uuid4
from unittest.mock import Mock, call
from datetime import datetime
from src.users.application.use_cases.create_user import CreateUser
from src.users.domain.entities import User

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def mock_encryption():
    return Mock()

@pytest.fixture
def mock_hashing():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository,
    mock_hashing,
    mock_encryption
):
    return CreateUser(
        repository=mock_repository,
        hashing=mock_hashing,
        encryption=mock_encryption
    )

@pytest.fixture
def user_in_db():
    return User(
        user_id=uuid4(),
        name="test",
        email="email@gmail.com",
        email_hash="hash",
        password="hash",
        created_at=datetime.now(),
        last_login=datetime.now()
    )

@pytest.fixture
def hash_password():
    return "hashed"

@pytest.fixture
def hash_search():
    return "hashed_search"

@pytest.fixture
def encrypted():
    return "encrypted"

@pytest.fixture
def decrypted():
    return "decrypted"

def test_create_user_success(
    use_case: CreateUser,
    mock_repository,
    mock_hashing,
    mock_encryption,
    encrypted,
    decrypted,
    hash_password,
    hash_search,
    user_in_db
):
    
    name = "test"
    email = "testemail"
    password = "pswd"
    
    mock_encryption.encrypt.return_value = encrypted
    mock_encryption.decrypt.return_value = decrypted
    mock_repository.create.return_value = user_in_db
    mock_hashing.hash_for_search.return_value = hash_search
    mock_hashing.hash_password.return_value = hash_password

    result = use_case.execute(
        name=name,
        email=email,
        password=password
    )

    mock_hashing.hash_password.assert_called_once_with(password=password)
    mock_hashing.hash_for_search.assert_called_once_with(data=email)
    assert mock_encryption.encrypt.call_count == 2
    mock_encryption.encrypt.assert_has_calls([
        call(name),
        call(email)
    ])

    assert result.name == decrypted
    assert result.email == decrypted



