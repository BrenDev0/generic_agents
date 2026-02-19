from fastapi import APIRouter, Request, Body, Depends
from src.security import fastapi_hmac_verification
from ...domain import Message, CreateMessageRequest
from ...application import CreateMessage
from ...dependencies import get_create_message_use_case

router = APIRouter(
    prefix="/messages",
    default=[Depends(fastapi_hmac_verification)]
)

@router.post("/", status_code=200, response_model=Message)
def create_message(
    request: Request,
    data: CreateMessageRequest = Body(...) ,
    use_case: CreateMessage = Depends(get_create_message_use_case)
):

    return use_case.execute(
        data=data
    )   