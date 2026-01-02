import strawberry
from src.features.users.interface.strawberry.queries import UserQueries
from src.features.users.interface.strawberry.mutations import UserMutations
from src.features.email.interface.strawberry.mutations import EmailMutations
from src.features.agents.interface.strawberry.queries import AgentQueries
from src.features.agents.interface.strawberry.mutations import AgentMutations
from src.features.agent_settings.interface.strawberry.queries import AgentSettingsQueries
from src.features.agent_settings.interface.strawberry.mutations import AgentSettingsMutations

@strawberry.type
class Query():
    @strawberry.field
    def users(self) -> UserQueries:
        return UserQueries()
    
    @strawberry.field
    def agents(self) -> AgentQueries:
        return AgentQueries()
    
    @strawberry.field
    def agent_settings(self) -> AgentSettingsQueries:
        return AgentSettingsQueries()


@strawberry.type
class Mutation():
    @strawberry.field
    def email(self) -> EmailMutations:
        return EmailMutations()

    @strawberry.field
    def users(self) -> UserMutations:
        return UserMutations()
    
    @strawberry.field
    def agents(self) -> AgentMutations:
        return AgentMutations()
    
    @strawberry.field
    def agent_settings(self) -> AgentSettingsMutations:
        return AgentSettingsMutations()

schema = strawberry.Schema(query=Query, mutation=Mutation)