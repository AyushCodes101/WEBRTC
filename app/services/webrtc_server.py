import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
from fastapi import WebSocket
from app.config.logger import logger

class WebRTCServer:
    def __init__(self):
        self.pc = RTCPeerConnection()

    async def process_offer(self, sdp: str, type: str):
        try:
            offer = RTCSessionDescription(sdp, type)
            await self.pc.setRemoteDescription(offer)

            answer = await self.pc.createAnswer()
            await self.pc.setLocalDescription(answer)

            return self.pc.localDescription
        except Exception as e:
            logger.error(f"Error processing WebRTC offer: {e}")
            return None