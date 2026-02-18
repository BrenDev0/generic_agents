import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from src.features.knowledge_base.domain.entities import Knowledge
from src.features.knowledge_base.domain.schemas import CreateKnowledgeRequest
from src.features.knowledge_base.application.use_cases.upload import UploadKnowledge
from src.features.agents.domain.entities import Agent

@pytest.fixture
def mock_data_repository():
    return Mock()

@pytest.fixture
def mock_agent_repository():
    return Mock()


@pytest.fixture
def mock_file_repository():
    return Mock()

@pytest.fixture
def mock_http_client():
    return Mock()

@pytest.fixture
def use_case(
    mock_data_repository,
    mock_file_repository,
    mock_agent_repository
):
    return UploadKnowledge(
        data_repository=mock_data_repository,
        file_repository=mock_file_repository,
        agent_repository=mock_agent_repository
    )


def test_success(
    mock_data_repository,
    mock_file_repository,
    mock_agent_repository,
    use_case: UploadKnowledge
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

    mock_agent_repository.get_one.return_value = fake_agent

    fake_knowledge = Knowledge(
        knowledge_id=knowledge_id,
        agent_id=agent_id,
        type="file",
        name="test",
        description="menu",
        url=None,
        state="test",
        created_at=datetime.now(),
        agent=fake_agent
    )
    fake_url = "url"

    fake_updated_knowledge = Knowledge(
        knowledge_id=knowledge_id,
        agent_id=agent_id,
        name="test",
        type="file",
        description="menu",
        url=fake_url,
        state="test",
        created_at=datetime.now(),
        agent=fake_agent
    )
    fake_req = CreateKnowledgeRequest(description="menu")
    file_bytes = b"fake file content"
    
    mock_data_repository.create.return_value = fake_knowledge
    mock_file_repository.upload.return_value = fake_url
    mock_data_repository.update.return_value = fake_updated_knowledge

    result = use_case.execute(
        req_data=fake_req,
        agent_id=agent_id,
        user_id=user_id,
        filename="test",
        file_type="...",
        file_bytes=file_bytes
    )

    mock_data_repository.create.assert_called_once()
    mock_file_repository.upload.assert_called_once_with(
        key=f"{user_id}/knowledge_base/{agent_id}/{knowledge_id}",
        file_bytes=file_bytes,
        content_type="file"
    )

    mock_data_repository.update.assert_called_once_with(
        key="knowledge_id",
        value=knowledge_id,
        changes={
            "url": fake_url
        }
    )

    assert result.knowledge_id == knowledge_id
    assert result.agent_id == agent_id
