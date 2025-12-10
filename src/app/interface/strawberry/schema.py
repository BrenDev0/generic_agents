import strawberry
from src.users.interface.strawberry.queries import UserQuery
from src.users.interface.strawberry.mutations import UserMutation

@strawberry.type
class Query(
    UserQuery
):
    pass


@strawberry.type
class Mutation(
    UserMutation
):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)