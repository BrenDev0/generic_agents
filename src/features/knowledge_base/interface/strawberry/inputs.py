import strawberry
from src.features.knowledge_base.domain.schemas import (
    CreateKnowledgeRequest
)

@strawberry.experimental.pydantic.input(CreateKnowledgeRequest, all_fields=True)
class CreateKnowledgeInput:
    pass