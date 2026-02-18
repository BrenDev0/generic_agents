import strawberry
from ...domain import (
    CreateKnowledgeRequest,
    UpdateKnowledgeRequest
)

@strawberry.experimental.pydantic.input(CreateKnowledgeRequest, all_fields=True)
class CreateKnowledgeInput:
    pass

@strawberry.experimental.pydantic.input(UpdateKnowledgeRequest, fields=["name", "description"])
class UpdateKnowledgeInput:
    pass