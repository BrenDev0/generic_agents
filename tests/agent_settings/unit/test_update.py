import pytest
from unittest.mock import Mock
from uuid import uuid4
from  datetime import datetime
from src.security.domain.exceptions import PermissionsException
from src.persistence.domain.exceptions import NotFoundException
from src.agent_settings.application.use_cases.update import UpdateAgentSettings
from src.agent_settings.domain.entities import AgentSettings
from src.agents.domain.entities import Agent
from src.agent_settings.domain.schemas import UpdateSettingsRequest

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
):
    return UpdateAgentSettings(
        settings_repository=mock_repository
    )


def test_success(
    mock_repository,
    use_case: UpdateAgentSettings
):
    setting_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()
    fake_settings = AgentSettings(
        setting_id=setting_id,
        agent_id=agent_id,
        system_prompt="...",
        temperature=0.2,
        transcripts=False,
        agent=Agent(
            agent_id=agent_id,
            user_id=user_id,
            name="...",
            description="...",
            created_at=datetime.now()
        )
    )

    mock_repository.get_one.return_value = fake_settings

    changes = UpdateSettingsRequest(
        system_prompt="updated"
    ) 

    fake_updated_settings = AgentSettings(
        setting_id=setting_id,
        agent_id=agent_id,
        system_prompt="updated",
        temperature=0.2,
        transcripts=False,
        agent=Agent(
            agent_id=agent_id,
            user_id=user_id,
            name="...",
            description="...",
            created_at=datetime.now()
        )
    )

    mock_repository.update.return_value = fake_updated_settings

    result = use_case.execute(
        settings_id=setting_id,
        user_id=user_id,
        changes=changes
    )

    mock_repository.get_one.assert_called_once_with(
        key="setting_id",
        value=setting_id
    )

    mock_repository.update.assert_called_once_with(
        key="setting_id",
        value=setting_id,
        changes=changes.model_dump(exclude_none=True, by_alias=False)
    )

    assert result.system_prompt == "updated"



def test_not_found(
    mock_repository,
    use_case: UpdateAgentSettings
):
    setting_id = uuid4()
    user_id = uuid4()

    mock_repository.get_one.return_value = None
    changes = UpdateSettingsRequest(
        system_prompt="updated"
    ) 

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            settings_id=setting_id,
            user_id=user_id,
            changes=changes
        )

    mock_repository.update.assert_not_called()
    assert "Settings not found" in str(exc_info)


def test_permissions_error(
    mock_repository,
    use_case: UpdateAgentSettings
):
    setting_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()
    fake_settings = AgentSettings(
        setting_id=setting_id,
        agent_id=agent_id,
        system_prompt="...",
        temperature=0.2,
        transcripts=False,
        agent=Agent(
            agent_id=agent_id,
            user_id=uuid4(),
            name="...",
            description="...",
            created_at=datetime.now()
        )
    )

    mock_repository.get_one.return_value = fake_settings
    changes = UpdateSettingsRequest(
        system_prompt="updated"
    ) 


    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            settings_id=setting_id,
            changes=changes
        )
    
    mock_repository.update.assert_not_called()
    assert "Forbidden" in str(exc_info)