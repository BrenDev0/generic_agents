from fastapi import APIRouter, Depends, Request, Body
from src.security import fastapi_hmac_verification
from ...domain import ChatPublic, CreateChatRequest
from ...application import CreateChat
from ...dependencies import get_create_chat_use_case

router = APIRouter(
    prefix="/chats",
    dependencies=[Depends(fastapi_hmac_verification)]
)

@router.post("/", status_code=201, response_model=ChatPublic)
def create_chat(
    request: Request,
    data: CreateChatRequest = Body(...),
    use_case: CreateChat = Depends(get_create_chat_use_case)
):
    return use_case.execute(
        agent_id=data.agent_id,
        chat_id=data.chat_id
    )

