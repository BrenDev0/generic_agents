import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from src.security.domain.exceptions import PermissionsException
from src.persistence.domain.exceptions import NotFoundException
from src.features.knowledge_base.application.use_cases.update import UpdateKnowledge
from src.features.knowledge_base.domain.entities import Knowledge
from src.features.agents.domain.entities import Agent
from src.features.knowledge_base.domain.schemas import UpdateKnowledgeRequest

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
):
    return UpdateKnowledge(
        repository=mock_repository
    )


def test_success(
    mock_repository,
    use_case: UpdateKnowledge
):
    knowledge_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()

    changes = UpdateKnowledgeRequest(
        description="updated description"
    )

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
        description="original description",
        url="https://s3.amazonaws.com/bucket/file.pdf",
        state="test",
        created_at=datetime.now(),
        agent=fake_agent
    )

    fake_updated_knowledge = Knowledge(
        knowledge_id=knowledge_id,
        agent_id=agent_id,
        type="file",
        name="test.pdf",
        description="updated description",
        url="https://s3.amazonaws.com/bucket/file.pdf",
        state="test",
        created_at=datetime.now(),
        agent=fake_agent
    )

    mock_repository.get_one.return_value = fake_knowledge
    mock_repository.update.return_value = fake_updated_knowledge

    result = use_case.execute(
        user_id=user_id,
        knowledge_id=knowledge_id,
        changes=changes
    )

    mock_repository.get_one.assert_called_once_with(
        key="knowledge_id",
        value=knowledge_id
    )

    mock_repository.update.assert_called_once_with(
        key="knowledge_id",
        value=knowledge_id,
        changes=changes.model_dump(exclude_none=True)
    )

    assert result.description == "updated description"
    assert result.knowledge_id == knowledge_id


def test_not_found(
    mock_repository,
    use_case: UpdateKnowledge
):
    knowledge_id = uuid4()
    user_id = uuid4()

    changes = UpdateKnowledgeRequest(
        description="updated description"
    )

    mock_repository.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            user_id=user_id,
            knowledge_id=knowledge_id,
            changes=changes
        )

    mock_repository.get_one.assert_called_once_with(
        key="knowledge_id",
        value=knowledge_id
    )

    mock_repository.update.assert_not_called()
    assert "404" in str(exc_info)


def test_permissions_error(
    mock_repository,
    use_case: UpdateKnowledge
):
    knowledge_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()

    changes = UpdateKnowledgeRequest(
        description="updated description"
    )

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
        description="original description",
        url="https://s3.amazonaws.com/bucket/file.pdf",
        state="test",
        created_at=datetime.now(),
        agent=fake_agent
    )

    mock_repository.get_one.return_value = fake_knowledge

    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            knowledge_id=knowledge_id,
            changes=changes
        )

    mock_repository.get_one.assert_called_once_with(
        key="knowledge_id",
        value=knowledge_id
    )

    mock_repository.update.assert_not_called()
    assert "403" in str(exc_info)