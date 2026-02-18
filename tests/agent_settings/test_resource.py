import pytest
from datetime import datetime
from  uuid import uuid4
from unittest.mock import Mock
from src.features.agent_settings.domain.entities import AgentSettings
from src.features.agents.domain.entities import Agent
from src.features.agent_settings.application.use_cases.resource import GetSettingsById
from src.security.domain.exceptions import PermissionsException
from src.persistence.domain.exceptions import NotFoundException


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def use_case(
    mock_repository
):
    return GetSettingsById(
        settings_repository=mock_repository
    )

def test_success(
    mock_repository,
    use_case: GetSettingsById
):
    
    user_id = uuid4()
    agent_id = uuid4()
    setting_id = uuid4()
    
    fake_setting = AgentSettings(
        setting_id=setting_id,
        agent_id=agent_id,
        system_prompt="...",
        temperature=0.5,
        transcripts=True,
        agent=Agent(
            agent_id=agent_id,
            user_id=user_id,
            name="...",
            description="...",
            created_at=datetime.now()
        )
    )

    mock_repository.get_one.return_value = fake_setting

    result = use_case.execute(
        user_id=user_id,
        agent_id=agent_id
    )

    mock_repository.get_one.assert_called_once_with(
        key="agent_id",
        value=agent_id
    )

    assert result.setting_id == setting_id


def test_not_found(
    mock_repository,
    use_case: GetSettingsById
):
    user_id = uuid4()
    agent_id = uuid4()
    mock_repository.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            user_id=user_id,
            agent_id=agent_id
        )

    
    assert "404" in str(exc_info)


def test_permissions_error(
    mock_repository,
    use_case: GetSettingsById
):
    user_id = uuid4()
    agent_id = uuid4()
    setting_id = uuid4()

    fake_setting = AgentSettings(
        setting_id=setting_id,
        agent_id=agent_id,
        system_prompt="...",
        temperature=0.5,
        transcripts=True,
        agent=Agent(
            agent_id=agent_id,
            user_id=uuid4(),
            name="...",
            description="...",
            created_at=datetime.now()
        )
    )


    mock_repository.get_one.return_value = fake_setting

    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            agent_id=agent_id
        )

    assert "403" in str(exc_info)