import pytest
from unittest.mock import Mock
from datetime import datetime
from uuid import uuid4
from src.agent_settings.application.use_cases.create import CreateAgentSettings
from src.agent_settings.domain.entities import AgentSettings
from src.agents.domain.entities import Agent
from src.agent_settings.domain.schemas import CreateSettingsRequest
from src.shared.domain.exceptions.repositories import NotFoundException
from src.shared.domain.exceptions.permissions import PermissionsException

@pytest.fixture
def mock_settings_repository():
    return Mock()

@pytest.fixture
def mock_agents_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_agents_repository,
    mock_settings_repository
):
    return CreateAgentSettings(
        agents_repository=mock_agents_repository,
        settings_repository=mock_settings_repository
    )

def test_success(
    mock_agents_repository,
    mock_settings_repository,
    use_case: CreateAgentSettings
):
    user_id = uuid4()
    agent_id = uuid4()

    fake_agent = Agent(
        agent_id=agent_id,
        user_id=user_id,
        name="fake",
        description="desc..",
        created_at=datetime.now()
    )

    fake_settings = AgentSettings(
        setting_id=uuid4(),
        agent_id=agent_id,
        system_prompt="system promt",
        temperature=0.5,
        transcripts=True
    )

    req_data = CreateSettingsRequest(
        system_prompt="system prompt",
        temperature=0.5,
        transcripts=True
    )

    mock_agents_repository.get_one.return_value = fake_agent
    mock_settings_repository.create.return_value = fake_settings

    result = use_case.execute(
        user_id=user_id,
        agent_id=agent_id,
        settings=req_data
    )

    mock_agents_repository.get_one.assert_called_once_with(
        key="agent_id",
        value=agent_id
    )

    mock_settings_repository.create.assert_called_once()

    assert result.setting_id == fake_settings.setting_id


def test_agent_not_found(
    mock_agents_repository,
    mock_settings_repository,
    use_case: CreateAgentSettings
):
    user_id = uuid4()
    agent_id = uuid4()

    req_data = CreateSettingsRequest(
        system_prompt="system prompt",
        temperature=0.5,
        transcripts=True
    )

    mock_agents_repository.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            user_id=user_id,
            agent_id=agent_id,
            settings=req_data
        )

    mock_agents_repository.get_one.assert_called_once_with(
        key="agent_id",
        value=agent_id
    )

    mock_settings_repository.create.assert_not_called()

    assert "Agent not found" in str(exc_info)


def test_permission_error(
    mock_agents_repository,
    mock_settings_repository,
    use_case: CreateAgentSettings
):
    user_id = uuid4()
    agent_id = uuid4()

    fake_agent = Agent(
        agent_id=agent_id,
        user_id=uuid4(),
        name="fake",
        description="desc..",
        created_at=datetime.now()
    )

    req_data = CreateSettingsRequest(
        system_prompt="system prompt",
        temperature=0.5,
        transcripts=True
    )

    mock_agents_repository.get_one.return_value = fake_agent

    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            agent_id=agent_id,
            settings=req_data
        )
    
    mock_settings_repository.create.assert_not_called()

    assert "Forbidden" in str(exc_info)

