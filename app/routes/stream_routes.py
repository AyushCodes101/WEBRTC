import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

# Configure Logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket connection for real-time video streaming.
    """
    await websocket.accept()
    logger.info("WebSocket connection accepted")

    try:
        while True:
            try:
                data = await websocket.receive_json()  # Expecting JSON data
                logger.info(f"Received data: {data}")
                
                if data.get("action") == "close":
                    logger.info("Client requested WebSocket closure")
                    break  # Stop loop without extra close attempt

                await websocket.send_json({"message": f"Received: {data}"})

            except WebSocketDisconnect:
                logger.warning("WebSocket disconnected by client")
                return  # Exit function cleanly, avoiding double close

    except Exception as e:
        logger.error(f"WebSocket error: {e}")

    finally:
        logger.info("WebSocket handler finished execution")
