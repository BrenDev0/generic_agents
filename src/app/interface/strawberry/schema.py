import strawberry
from src.users.interface.strawberry.queries import UserQueries
from src.users.interface.strawberry.mutations import UserMutations
from src.email.interface.strawberry.mutations import EmailMutations
from src.agents.interface.strawberry.queries import AgentQueries

@strawberry.type
class Query():
    @strawberry.field
    def users(self) -> UserQueries:
        return UserQueries()
    
    @strawberry.field
    def agents(self) -> AgentQueries:
        return AgentQueries()


@strawberry.type
class Mutation():
    @strawberry.field
    def email(self) -> EmailMutations:
        return EmailMutations()

    @strawberry.field
    def users(self) -> UserMutations:
        return UserMutations()


schema = strawberry.Schema(query=Query, mutation=Mutation)