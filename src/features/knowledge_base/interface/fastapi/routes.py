import logging
from fastapi import APIRouter, Depends, Body, HTTPException
from uuid import UUID
from src.security import fastapi_hmac_verification
from ...domain import UpdateKnowledgeRequest, InternalUpdateEmbeddingStatus, KnowledgePublic
from ...dependencies import get_update_knowledge_use_case

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/knowledge-base",
    dependencies=[Depends(fastapi_hmac_verification)]
)

@router.patch(path="/embedding-status/{knowledge_id}", status_code=200, response_model=KnowledgePublic)
def update_embedding_status(
    knowledge_id: UUID,
    data: InternalUpdateEmbeddingStatus = Body(...)
):
    use_case = get_update_knowledge_use_case()
    changes = UpdateKnowledgeRequest(
        state=data.status
    )
    return use_case.execute(
        user_id=data.user_id,
        knowledge_id=knowledge_id,
        changes=changes
    )
    
