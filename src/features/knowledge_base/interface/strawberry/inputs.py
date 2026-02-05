import strawberry
from src.features.knowledge_base.domain.schemas import (
    CreateKnowledgeRequest,
    UpdateKnowledgeRequest
)

@strawberry.experimental.pydantic.input(CreateKnowledgeRequest, all_fields=True)
class CreateKnowledgeInput:
    pass

@strawberry.experimental.pydantic.input(UpdateKnowledgeRequest, fields=["name", "description"])
class UpdateKnowledgeInput:
    pass