import pytest 
from uuid import uuid4
from datetime import datetime
from unittest.mock import Mock
from src.security.domain.exceptions import PermissionsException
from src.features.knowledge_base.application.use_cases.collection import GetKnowledgeCollection
from src.features.knowledge_base.domain.entities import Knowledge
from src.features.agents.domain.entities import Agent

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
):
    return GetKnowledgeCollection(data_repository=mock_repository)


def test_success(
    mock_repository,
    use_case: GetKnowledgeCollection
):
    user_id = uuid4()
    agent_id = uuid4()

    fake_agent = Agent(
        agent_id=agent_id,
        user_id=user_id,
        name="test agent",
        description="test",
        created_at=datetime.now()
    )

    mock_collection = [
        Knowledge(
            knowledge_id=uuid4(),
            agent_id=agent_id,
            type="file",
            name="document_1.pdf",
            description="test document 1",
            url="https://s3.amazonaws.com/bucket/file1.pdf",
            is_embedded=True,
            created_at=datetime.now(),
            agent=fake_agent
        ),
        Knowledge(
            knowledge_id=uuid4(),
            agent_id=agent_id,
            type="web",
            name="website",
            description="test website",
            url="https://example.com",
            is_embedded=False,
            created_at=datetime.now(),
            agent=fake_agent
        )
    ]

    mock_repository.get_many.return_value = mock_collection

    result = use_case.execute(
        user_id=user_id,
        agent_id=agent_id
    )

    mock_repository.get_many.assert_called_once_with(
        key="agent_id",
        value=agent_id
    )
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].agent_id == agent_id
    assert result[1].agent_id == agent_id


def test_no_results(
    mock_repository,
    use_case: GetKnowledgeCollection
):
    user_id = uuid4()
    agent_id = uuid4()
    mock_repository.get_many.return_value = None

    result = use_case.execute(
        user_id=user_id,
        agent_id=agent_id
    )

    assert isinstance(result, list)
    assert len(result) == 0

def test_wrong_permissions(
    mock_repository,
    use_case: GetKnowledgeCollection
):
    user_id = uuid4()
    agent_id = uuid4()

    fake_agent = Agent(
        agent_id=agent_id,
        user_id=uuid4(),  # Different user
        name="test agent",
        description="test",
        created_at=datetime.now()
    )

    mock_collection = [
        Knowledge(
            knowledge_id=uuid4(),
            agent_id=agent_id,
            type="file",
            name="document_1.pdf",
            description="test document 1",
            url="https://s3.amazonaws.com/bucket/file1.pdf",
            is_embedded=True,
            created_at=datetime.now(),
            agent=fake_agent
        )
    ]

    mock_repository.get_many.return_value = mock_collection

    with pytest.raises(PermissionsException) as exc_info:
        result = use_case.execute(
            user_id=user_id,
            agent_id=agent_id
        )

    assert "Forbidden" in str(exc_info)