import strawberry
from src.users.interface.strawberry.queries import UserQuery

@strawberry.type
class Query(UserQuery):
    pass


schema = strawberry.Schema(query=Query)