import strawberry
from src.features.knowledge_base.domain.schemas import KnowledgePublic

@strawberry.experimental.pydantic.type(KnowledgePublic, all_fields=True)
class KnowledgeType:
    pass