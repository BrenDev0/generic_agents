import logging
import strawberry
from uuid import UUID
from strawberry.file_uploads import Upload
from src.app.domain.exceptions import GraphQlException
from src.features.knowledge_base.domain.exceptions import UnsupportedFileType
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.features.knowledge_base.dependencies.use_cases import (
    get_upload_knowledge_use_case
)
from src.features.knowledge_base.dependencies.business_rules import get_supported_file_type_rule
from src.features.knowledge_base.interface.strawberry.inputs import (
    CreateKnowledgeInput
)
from src.features.knowledge_base.interface.strawberry.types import KnowledgeType
logger = logging.getLogger(__name__)

@strawberry.type
class KnowledgeBaseMutaions:
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Upload a document for an agents knowledgebase"
    )
    async def upload_knowledge(
        self, 
        info: strawberry.Info,
        agent_id: UUID,
        input: CreateKnowledgeInput,
        file: Upload # type: ignore
    ) -> KnowledgeType:
        user_id = info.context.get("user_id")
        is_supported_file_type = get_supported_file_type_rule()
        use_case = get_upload_knowledge_use_case()

        try:
            filename = file.filename
            if not filename:
                raise GraphQlException("Filename is required")
            
            file_type = file.content_type
            if not file_type:
                raise GraphQlException("File content type is required")

            is_supported_file_type.validate(
                file_type=file_type
            )

            data = await file.read()
            
            return use_case.execute(
                req_data=input.to_pydantic(),
                user_id=user_id,
                agent_id=agent_id,
                filename=filename,
                file_bytes=data
            )
        
        except UnsupportedFileType as e:
            raise GraphQlException(str(e))

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()