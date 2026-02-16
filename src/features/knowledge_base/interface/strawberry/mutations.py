import logging
import strawberry
from strawberry.file_uploads import Upload
from starlette.datastructures import UploadFile
from uuid import UUID
from src.app.interface.strawberry.decorators.req_validation import validate_input_to_model
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.features.knowledge_base.dependencies import use_cases, business_rules
from src.features.knowledge_base.domain import exceptions, schemas, entities
from src.features.knowledge_base.interface.strawberry import types, inputs
from src.features.sessions.dependencies.use_cases import get_update_embeddings_tracker_use_case
logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 50 * 1024 * 1024 


@strawberry.type
class KnowledgeBaseMutaions:
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Upload file"
    )
    @validate_input_to_model
    async def upload_knowledge(
        self,
        agent_id: UUID,
        info: strawberry.Info,
        file: Upload,
        input: inputs.CreateKnowledgeInput,
        embed_document: bool = False
    ) -> types.KnowledgeType:
        if not isinstance(file, UploadFile):
            raise GraphQlException(f"Type {type(file).__name__} invalid for vairable file, Expected type Upload!")
        
        try:
            user_id = info.context.get("user_id")
            use_case = use_cases.get_upload_knowledge_use_case()
            is_supported_file_type = business_rules.get_supported_file_type_rule() 

            filename = file.filename.lower().replace(" ", "_")
            content_type = file.content_type

            is_supported_file_type.validate(
                file_type=content_type
            )

            file_bytes = await file.read()
            if len(file_bytes) > MAX_FILE_SIZE:
                raise GraphQlException("File too large. Max size is 10MB.")

            if embed_document:
                input.state = "PROCESANDO"

            saved_doc = use_case.execute(
                req_data=input,
                user_id=user_id,
                agent_id=agent_id,
                filename=filename,
                file_type=content_type,
                file_bytes=file_bytes
            )

            if embed_document:
                if not input.connection_id:
                    raise PermissionsException("Cannot embed document without connection id")
                
                send_to_embed = use_cases.get_send_to_embed_use_case()
                update_embedding_tracker = get_update_embeddings_tracker_use_case()
                
                embedding_status = {
                    "stage": "Enviando documento...",
                    "status": "Enviando",
                    "progress": 10 # progress of the whole process, 5 parts of  20%
                }

                update_embedding_tracker.execute(
                    agent_id=saved_doc.agent_id,
                    knowledge_id=saved_doc.knowledge_id,
                    update=embedding_status
                )

                await send_to_embed.execute(
                    user_id=user_id,
                    agent_id=saved_doc.agent_id,
                    knowledge_id=saved_doc.knowledge_id,
                    connection_id=input.connection_id,
                    file_type=saved_doc.type,
                    file_url=saved_doc.url
                )

                embedding_status = {
                    "stage": "Enviando documento...",
                    "status": "Enviado",
                    "progress": 20  
                }

                update_embedding_tracker.execute(
                    agent_id=saved_doc.agent_id,
                    knowledge_id=saved_doc.knowledge_id,
                    update=embedding_status
                )

            return saved_doc
        
        except (NotFoundException, PermissionsException, exceptions.UnsupportedFileType) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
    



    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Update Knowledge resource"
    )
    @validate_input_to_model
    def update_knowledge(
        self,
        knowledge_id: UUID,
        info: strawberry.Info,
        input: inputs.UpdateKnowledgeInput
    ) -> types.KnowledgeType:
        try:
            user_id = info.context.get("user_id")
            use_case = use_cases.get_update_knowledge_use_case()

            return use_case.execute(
                user_id=user_id,
                knowledge_id=knowledge_id,
                changes=input
            )

        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    


    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Delete knowledge resource"
    )
    async def delete_knowledge(
        self,
        knowledge_id: UUID,
        info: strawberry.Info
    ) -> types.KnowledgeType:
        try:
            user_id = info.context.get("user_id")
            use_case = use_cases.get_delete_knowledge_use_case()

        
            return await use_case.execute(
                knowledge_id=knowledge_id,
                user_id=user_id
            )
        
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e: 
            logger.error(str(e))
            raise GraphQlException()



    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Delete from vector base"
    )
    async def delete_embeddings(
        self,
        knowledge_id: UUID,
        info: strawberry.Info
    ) -> types.KnowledgeType:
        try:
            user_id = info.context.get("user_id")
            resource_use_case = use_cases.get_knowledge_resource_use_case()
            
            resource: entities.Knowledge = resource_use_case.execute(
                user_id=user_id,
                knowledge_id=knowledge_id
            )

            remove_embeddings_use_case = use_cases.get_delete_embeddings_use_case()

            await remove_embeddings_use_case.execute(
                knowledge_id=resource.knowledge_id
            )

            update_knowledge_use_case = use_cases.get_update_knowledge_use_case()
            changes = schemas.UpdateKnowledgeRequest(
                state="NO PROCESADO"
            )
            return update_knowledge_use_case.execute(
                user_id=user_id,
                knowledge_id=resource.knowledge_id,
                changes=changes
            )


        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e: 
            logger.error(str(e))
            raise GraphQlException()
        


    
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="create embeddings"
    )
    async def create_embeddings(
        self,
        knowledge_id: UUID,
        connection_id: UUID,
        info: strawberry.Info
    ) -> types.KnowledgeType:
        try:
            user_id = info.context.get("user_id")
            resource_use_case = use_cases.get_knowledge_resource_use_case()
            
            resource: entities.Knowledge = resource_use_case.execute(
                user_id=user_id,
                knowledge_id=knowledge_id
            )

            send_to_embed_use_case = use_cases.get_send_to_embed_use_case()
            await send_to_embed_use_case.execute(
                user_id=user_id,
                agent_id=resource.agent_id,
                knowledge_id=resource.knowledge_id,
                connection_id=connection_id,
                file_type=resource.type,
                file_url=resource.url
            )

            update_use_case = use_cases.get_update_knowledge_use_case()
            changes = schemas.UpdateKnowledgeRequest(
                state="PROCESANDO"
            )
            updated = update_use_case.execute(
                user_id=user_id, 
                knowledge_id=resource.knowledge_id,
                changes=changes
            )

            return updated


        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e: 
            logger.error(str(e))
            raise GraphQlException()