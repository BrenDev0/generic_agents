import strawberry
from starlette.datastructures import UploadFile
from strawberry.file_uploads import Upload
from src.features.users.interface.strawberry import queries as user_queries, mutations as user_mutations
from src.features.email.interface.strawberry.mutations import EmailMutations
from src.features.agents.interface.strawberry.mutations import AgentMutations
from src.features.agents.interface.strawberry.queries import AgentQueries
from src.features.agent_settings.interface.strawberry.mutations import AgentSettingsMutations
from src.features.agent_settings.interface.strawberry.queries import AgentSettingsQueries
from src.features.knowledge_base.interface.strawberry.mutations import KnowledgeBaseMutaions
from src.features.knowledge_base.interface.strawberry.queries import KnowledgeQueries

@strawberry.type
class Query():
    @strawberry.field
    def users(self) -> user_queries.UserQueries:
        return user_queries.UserQueries()
    
    @strawberry.field
    def agents(self) -> AgentQueries:
        return AgentQueries()
    
    @strawberry.field
    def agent_settings(self) -> AgentSettingsQueries:
        return AgentSettingsQueries()
    
    @strawberry.field
    def knowledge_base(self) -> KnowledgeQueries:
        return KnowledgeQueries()


@strawberry.type
class Mutation():
    @strawberry.field
    def email(self) -> EmailMutations:
        return EmailMutations()

    @strawberry.field
    def users(self) -> user_mutations.UserMutations:
        return user_mutations.UserMutations()
    
    @strawberry.field
    def agents(self) -> AgentMutations:
        return AgentMutations()
    
    @strawberry.field
    def agent_settings(self) -> AgentSettingsMutations:
        return AgentSettingsMutations()
    
    @strawberry.field
    def knowledge_base(self) -> KnowledgeBaseMutaions:
        return KnowledgeBaseMutaions()

schema = strawberry.Schema(
    query=Query, 
    mutation=Mutation,
    scalar_overrides={UploadFile: Upload}
)