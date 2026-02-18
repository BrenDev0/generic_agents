import strawberry
from ...domain import KnowledgePublic

@strawberry.experimental.pydantic.type(KnowledgePublic, all_fields=True)
class KnowledgeType:
    pass