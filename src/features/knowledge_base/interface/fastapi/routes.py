import logging
from fastapi import APIRouter, Depends, Body, HTTPException
from uuid import UUID
from src.app.interface.fastapi.middleware.hmac import verify_hmac
from src.features.knowledge_base.domain.schemas import UpdateKnowledgeRequest, InternalUpdateEmbeddingStatus, KnowledgePublic
from src.features.knowledge_base.dependencies.use_cases import get_update_knowledge_use_case

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/knowledge-base",
    dependencies=[Depends(verify_hmac)]
)

@router.patch(path="/ebedding-status/{knowledge_id}", status_code=200, response_model=KnowledgePublic)
def update_embedding_status(
    knowledge_id: UUID,
    data: InternalUpdateEmbeddingStatus = Body(...)
):
    try:
        use_case = get_update_knowledge_use_case()
        changes = UpdateKnowledgeRequest(
            is_embedded=data.status
        )
        return use_case.execute(
            user_id=data.user_id,
            knowledge_id=knowledge_id,
            changes=changes
        )
    
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Unable to proccess request at this time")