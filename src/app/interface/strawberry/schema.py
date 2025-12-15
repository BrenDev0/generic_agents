import strawberry
from src.users.interface.strawberry.queries import UserQuery
from src.users.interface.strawberry.mutations import UserMutations
from src.email.interface.strawberry.mutations import EmailMutations

@strawberry.type
class Query(
    UserQuery
):
    pass


@strawberry.type
class Mutation(
):
    @strawberry.field
    def email(self) -> EmailMutations:
        return EmailMutations()

    @strawberry.field
    def users(self) -> UserMutations:
        return UserMutations()


schema = strawberry.Schema(query=Query, mutation=Mutation)