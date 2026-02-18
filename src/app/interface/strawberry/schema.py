import strawberry
from starlette.datastructures import UploadFile
from strawberry.file_uploads import Upload
from src.features.users.interface.strawberry import queries as user_queries, mutations as user_mutations
from src.features.email.interface.strawberry.mutations import EmailMutations
from src.features.agents.interface.strawberry import queries as agent_queries, mutations as agent_mutations
from src.features.agent_settings.interface.strawberry import queries as agent_settings_queries, mutations as agent_settings_mutations
from src.features.knowledge_base.interface.strawberry import queries as knowledge_base_queries, mutations as knowledge_base_mutations
from src.features.chats.interface.strawberry import mutations as chat_mutations

@strawberry.type
class Query():
    @strawberry.field
    def users(self) -> user_queries.UserQueries:
        return user_queries.UserQueries()
    
    @strawberry.field
    def agents(self) -> agent_queries.AgentQueries:
        return agent_queries.AgentQueries()
    
    @strawberry.field
    def agent_settings(self) -> agent_settings_queries.AgentSettingsQueries:
        return agent_settings_queries.AgentSettingsQueries()
    
    @strawberry.field
    def knowledge_base(self) -> knowledge_base_queries.KnowledgeQueries:
        return knowledge_base_queries.KnowledgeQueries()


@strawberry.type
class Mutation():
    @strawberry.field
    def email(self) -> EmailMutations:
        return EmailMutations()

    @strawberry.field
    def users(self) -> user_mutations.UserMutations:
        return user_mutations.UserMutations()
    
    @strawberry.field
    def agents(self) -> agent_mutations.AgentMutations:
        return agent_mutations.AgentMutations()
    
    @strawberry.field
    def agent_settings(self) -> agent_settings_mutations.AgentSettingsMutations:
        return agent_settings_mutations.AgentSettingsMutations()
    
    @strawberry.field
    def knowledge_base(self) -> knowledge_base_mutations.KnowledgeBaseMutaions:
        return knowledge_base_mutations.KnowledgeBaseMutaions()
    
    @strawberry.field
    def chats(self) -> chat_mutations.ChatMutations:
        return chat_mutations.ChatMutations()

schema = strawberry.Schema(
    query=Query, 
    mutation=Mutation,
    scalar_overrides={UploadFile: Upload}
)