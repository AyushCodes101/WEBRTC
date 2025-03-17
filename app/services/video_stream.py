import logging
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from av import VideoFrame
import cv2

# Configure Logging
logger = logging.getLogger(__name__)

router = APIRouter()
pcs = set()  # Stores all active peer connections

class VideoTrack(VideoStreamTrack):
    """Represents an incoming video stream with a mirror (flipped) effect."""

    def __init__(self, track):
        super().__init__()
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        
        # Convert frame to NumPy array (BGR format)
        img = frame.to_ndarray(format="bgr24")

        # Check if the image was correctly received
        if img is None or img.shape[0] == 0:
            logger.error("Received an empty frame!")
            return frame

        # Apply mirroring (flip horizontally)
        mirrored_img = cv2.flip(img, 1)  # Flip along the vertical axis

        # Convert back to VideoFrame
        flipped_frame = VideoFrame.from_ndarray(mirrored_img, format="bgr24")

        logger.info("Frame mirrored successfully")  # Debugging log
        return flipped_frame
    

@router.post("/offer")
async def offer(sdp: str, type: str):
    """
    Endpoint to handle SDP offer from the client.
    """
    try:
        pc = RTCPeerConnection()
        pcs.add(pc)

        offer = RTCSessionDescription(sdp, type)
        await pc.setRemoteDescription(offer)

        # Attach a media stream (video)
        for t in pc.getTransceivers():
            if t.kind == "video":
                pc.addTrack(VideoTrack(t.receiver.track))

        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        logger.info("SDP offer received and processed")
        return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}

    except Exception as e:
        logger.error(f"Error in offer handling: {e}")
        return {"error": str(e)}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket connection for real-time video streaming.
    """
    await websocket.accept()
    logger.info("WebSocket connection accepted")

    try:
        while True:
            data = await websocket.receive_text()
            
            if data.lower() == "close":  # If client requests closure
                logger.info("Client requested WebSocket closure")
                await websocket.close()
                return  # Exit function to prevent further execution
            
            await websocket.send_text(f"Received: {data}")

    except WebSocketDisconnect:
        logger.warning("WebSocket disconnected by client")

    except Exception as e:
        logger.error(f"WebSocket error: {e}")

    finally:
        try:
            await websocket.close()
            logger.info("WebSocket connection closed gracefully")
        except Exception:
            logger.warning("WebSocket was already closed, skipping closure.")