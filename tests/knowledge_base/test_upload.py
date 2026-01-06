import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from src.features.knowledge_base.domain.entities import Knowledge
from src.features.knowledge_base.domain.schemas import CreateKnowledgeRequest
from src.features.knowledge_base.application.use_cases.upload import UploadKnowledge

@pytest.fixture
def mock_data_repository():
    return Mock()

@pytest.fixture
def mock_file_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_data_repository,
    mock_file_repository
):
    return UploadKnowledge(
        data_repository=mock_data_repository,
        file_repository=mock_file_repository
    )

def test_success(
    mock_data_repository,
    mock_file_repository,
    use_case: UploadKnowledge
):
    knowledge_id = uuid4()
    user_id = uuid4()
    agent_id = uuid4()

    fake_knowledge = Knowledge(
        knowledge_id=knowledge_id,
        agent_id=agent_id,
        type="file",
        name="test",
        description="menu",
        url=None,
        is_embedded=True,
        created_at=datetime.now()
    )
    fake_url = "url"

    fake_updated_knowledge = Knowledge(
        knowledge_id=knowledge_id,
        agent_id=agent_id,
        type="file",
        description="menu",
        url=fake_url,
        is_embedded=True,
        created_at=datetime.now()
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
        file_bytes=file_bytes
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


def test_upload_error(
    mock_data_repository,
    mock_file_repository,
    use_case: UploadKnowledge
):
    
    knowledge_id = uuid4()
    user_id = uuid4()
    agent_id = uuid4()

    fake_knowledge = Knowledge(
        knowledge_id=knowledge_id,
        agent_id=agent_id,
        type="file",
        name="test",
        description="menu",
        url=None,
        is_embedded=True,
        created_at=datetime.now()
    )
    
    fake_req = CreateKnowledgeRequest(description="menu")
    file_bytes = b"fake file content"
    
    mock_data_repository.create.return_value = fake_knowledge
    mock_file_repository.upload.side_effect = Exception("S3 upload failed") 

    with pytest.raises(Exception):
        use_case.execute(
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
        file_bytes=file_bytes
    )

    mock_data_repository.update.assert_not_called()
    mock_data_repository.delete.assert_called_once_with(
        key="knowledge_id",
        value=knowledge_id
    )

def test_update_error(
    mock_data_repository,
    mock_file_repository,
    use_case: UploadKnowledge
): 
    knowledge_id = uuid4()
    user_id = uuid4()
    agent_id = uuid4()

    fake_knowledge = Knowledge(
        knowledge_id=knowledge_id,
        agent_id=agent_id,
        type="file",
        name="test",
        description="menu",
        url=None,
        is_embedded=True,
        created_at=datetime.now()
    )
    fake_url = "url"

    fake_req = CreateKnowledgeRequest(description="menu")
    file_bytes = b"fake file content"
    
    mock_data_repository.create.return_value = fake_knowledge
    mock_file_repository.upload.return_value = fake_url
    mock_data_repository.update.side_effect = Exception("...")

    with pytest.raises(Exception):
        use_case.execute(
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
        file_bytes=file_bytes
    )

    mock_data_repository.update.assert_called_once_with(
        key="knowledge_id",
        value=knowledge_id,
        changes={
            "url": fake_url
        }
    )

    mock_data_repository.delete.assert_called_once_with(
        key="knowledge_id",
        value=knowledge_id
    )

    mock_file_repository.delete.assert_called_once_with(
        key=f"{user_id}/knowledge_base/{agent_id}/{knowledge_id}"
    )
