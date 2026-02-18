import pytest
from uuid import uuid4
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.features.knowledge_base.application.use_cases.delete import DeleteKnowledge
from src.features.knowledge_base.domain.entities import Knowledge
from src.features.agents.domain.entities import Agent

@pytest.fixture
def mock_data_repository():
    return Mock()

@pytest.fixture
def mock_file_repository():
    return Mock()

@pytest.fixture
def mock_http_client():
    return AsyncMock()

@pytest.fixture
def use_case(
    mock_data_repository,
    mock_file_repository,
    mock_http_client
):
    return DeleteKnowledge(
        data_repository=mock_data_repository,
        file_repository=mock_file_repository,
        async_http_client=mock_http_client

    )

@pytest.mark.asyncio
@patch(
    "src.features.knowledge_base.application.use_cases.delete.generate_hmac_headers",
    return_value={
        "x-signature": "fake_signature",
        "x-payload": "fake_payload",
        "Content-Type": "application/json",
    },
) # Mock generate_hmac_headers
async def test_success_file_type(
    mock_generate_hmac_headers,
    mock_data_repository,
    mock_file_repository,
    use_case: DeleteKnowledge
):
    knowledge_id = uuid4()
    user_id = uuid4()
    agent_id = uuid4()

    fake_agent = Agent(
        agent_id=agent_id,
        user_id=user_id,
        name="test agent",
        description="test",
        created_at=datetime.now()
    )

    fake_knowledge = Knowledge(
        knowledge_id=knowledge_id,
        agent_id=agent_id,
        type="file",
        name="test.pdf",
        description="test document",
        url="https://s3.amazonaws.com/bucket/file.pdf",
        state="test",
        created_at=datetime.now(),
        agent=fake_agent
    )

    mock_data_repository.get_one.return_value = fake_knowledge
    mock_data_repository.delete.return_value = fake_knowledge

    result = await use_case.execute(
        knowledge_id=knowledge_id,
        user_id=user_id
    )

    mock_data_repository.get_one.assert_called_once_with(
        key="knowledge_id",
        value=knowledge_id
    )

    mock_file_repository.delete.assert_called_once_with(
        keys=[f"{user_id}/knowledge_base/{agent_id}/{knowledge_id}"]
    )

    mock_data_repository.delete.assert_called_once_with(
        key="knowledge_id",
        value=knowledge_id
    )

    assert result.knowledge_id == knowledge_id
    assert result.agent_id == agent_id

@pytest.mark.asyncio
@patch(
    "src.features.knowledge_base.application.use_cases.delete.generate_hmac_headers",
    return_value={
        "x-signature": "fake_signature",
        "x-payload": "fake_payload",
        "Content-Type": "application/json",
    },
)  # Mock generate_hmac_headers
async def test_success_web_type(
    mock_generate_hmac_headers,
    mock_data_repository,
    mock_file_repository,
    use_case: DeleteKnowledge
):
    knowledge_id = uuid4()
    user_id = uuid4()
    agent_id = uuid4()

    fake_agent = Agent(
        agent_id=agent_id,
        user_id=user_id,
        name="test agent",
        description="test",
        created_at=datetime.now()
    )

    fake_knowledge = Knowledge(
        knowledge_id=knowledge_id,
        agent_id=agent_id,
        type="web",
        name="website",
        description="test website",
        url="https://example.com",
        state="test",
        created_at=datetime.now(),
        agent=fake_agent
    )

    mock_data_repository.get_one.return_value = fake_knowledge
    mock_data_repository.delete.return_value = fake_knowledge

    result = await use_case.execute(
        knowledge_id=knowledge_id,
        user_id=user_id
    )

    mock_data_repository.get_one.assert_called_once_with(
        key="knowledge_id",
        value=knowledge_id
    )

    mock_file_repository.delete.assert_not_called()

    mock_data_repository.delete.assert_called_once_with(
        key="knowledge_id",
        value=knowledge_id
    )

    assert result.knowledge_id == knowledge_id
    assert result.agent_id == agent_id

@pytest.mark.asyncio
@patch(
    "src.features.knowledge_base.application.use_cases.delete.generate_hmac_headers",
    return_value={
        "x-signature": "fake_signature",
        "x-payload": "fake_payload",
        "Content-Type": "application/json",
    },
) # Mock generate_hmac_headers
async def test_not_found(
    mock_generate_hmac_headers,
    mock_data_repository,
    mock_file_repository,
    use_case: DeleteKnowledge
):
    knowledge_id = uuid4()
    user_id = uuid4()

    mock_data_repository.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        await use_case.execute(
            knowledge_id=knowledge_id,
            user_id=user_id
        )

    mock_data_repository.get_one.assert_called_once_with(
        key="knowledge_id",
        value=knowledge_id
    )

    mock_file_repository.delete.assert_not_called()
    mock_data_repository.delete.assert_not_called()
    assert "404" in str(exc_info)

@pytest.mark.asyncio
@patch(
    "src.features.knowledge_base.application.use_cases.delete.generate_hmac_headers",
    return_value={
        "x-signature": "fake_signature",
        "x-payload": "fake_payload",
        "Content-Type": "application/json",
    },
) # Mock generate_hmac_headers
async def test_permission_error(
    mock_generate_hmac_headers,
    mock_data_repository,
    mock_file_repository,
    use_case: DeleteKnowledge
):
    knowledge_id = uuid4()
    user_id = uuid4()
    agent_id = uuid4()

    fake_agent = Agent(
        agent_id=agent_id,
        user_id=uuid4(),  # Different user
        name="test agent",
        description="test",
        created_at=datetime.now()
    )

    fake_knowledge = Knowledge(
        knowledge_id=knowledge_id,
        agent_id=agent_id,
        type="file",
        name="test.pdf",
        description="test document",
        url="https://s3.amazonaws.com/bucket/file.pdf",
        state="test",
        created_at=datetime.now(),
        agent=fake_agent
    )

    mock_data_repository.get_one.return_value = fake_knowledge

    with pytest.raises(PermissionsException) as exc_info:
        await use_case.execute(
            knowledge_id=knowledge_id,
            user_id=user_id
        )

    mock_data_repository.get_one.assert_called_once_with(
        key="knowledge_id",
        value=knowledge_id
    )

    mock_file_repository.delete.assert_not_called()
    mock_data_repository.delete.assert_not_called()
    assert "403" in str(exc_info)