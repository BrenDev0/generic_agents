import logging
from fastapi import APIRouter, WebSocket, status, WebSocketDisconnect
from uuid import UUID
from src.websocket.interface.middleware.hmac import verify_hmac_ws
logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Websocket"]
)

router.websocket(path="/{chat_id}/{x_signature}/{x_payload}")
async def connect(
    chat_id: UUID,
    websocket: WebSocket,
    signature: str,
    payload: str
):
    if not await verify_hmac_ws(signature=signature, payload=payload):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Faild HMAC verification")
        return
        
    await websocket.accept()

    try: 
        while True:
            pass

    except WebSocketDisconnect:
        logger.debug(f'Websocket connection: {chat_id} closed.')

        


    

    