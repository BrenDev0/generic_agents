import logging
from uuid import UUID
from fastapi import UploadFile, Depends, Request, File, APIRouter, HTTPException, Form
from fastapi.security import HTTPBearer
from src.app.interface.fastapi.middleware import auth, hmac
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.features.knowledge_base.application.use_cases.upload import UploadKnowledge
from src.features.knowledge_base.application.rules.supported_file_types import IsSupportedFileType
from src.features.knowledge_base.dependencies import business_rules, use_cases
from src.features.knowledge_base.domain import exceptions, schemas
logger = logging.getLogger(__name__)


MAX_FILE_SIZE = 10 * 1024 * 1024
security = HTTPBearer()
router = APIRouter(
    prefix="/knowledge-base",
    dependencies=[Depends(security), Depends(hmac.verify_hmac)] 
)

@router.post(path="/upload", status_code=201, response_model=schemas.KnowledgePublic)
async def file_upload(
    req: Request,
    agent_id: UUID,
    description: str = Form(...),
    file: UploadFile = File(...),
    train_now: bool = False,
    _: None = Depends(auth.auth_middleware),
    use_case: UploadKnowledge = Depends(use_cases.get_upload_knowledge_use_case),
    is_supported_file_type: IsSupportedFileType = Depends(business_rules.get_supported_file_type_rule)
):
    try:
        user_id = req.state.user
        filename = file.filename.lower().replace(" ", "_")
        content_type = file.content_type

        is_supported_file_type.validate(
            file_type=content_type
        )

        file_bytes = await file.read()
        if len(file_bytes) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large. Max size is 10MB.")

        data = schemas.CreateKnowledgeRequest(
            description=description
        )
            
        return use_case.execute(
            req_data=data,
            user_id=user_id,
            agent_id=agent_id,
            filename=filename,
            file_type=content_type,
            file_bytes=file_bytes
        )
    
    except exceptions.UnsupportedFileType as e:
        raise HTTPException(status_code=400, detail=str(e))

    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except PermissionsException as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Unable to process request at this time")