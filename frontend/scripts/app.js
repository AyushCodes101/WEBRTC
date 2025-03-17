const startBtn = document.getElementById("startBtn");
const statusMessage = document.getElementById("statusMessage");
const localVideo = document.getElementById("localVideo");
const remoteVideo = document.getElementById("remoteVideo");

let pc = new RTCPeerConnection();
let ws = new WebSocket("ws://localhost:8000/ws");

statusMessage.innerText = "⚠️ Connection Not Started";

// WebSocket Events
ws.onopen = () => {
    statusMessage.innerText = "✅ WebSocket Connected";
    statusMessage.style.color = "green";
};

ws.onerror = () => {
    statusMessage.innerText = "❌ WebSocket Error";
    statusMessage.style.color = "red";
};

ws.onclose = () => {
    statusMessage.innerText = "❌ WebSocket Disconnected";
    statusMessage.style.color = "red";
};

// Start Video Streaming
startBtn.addEventListener("click", async () => {
    try {
        let stream = await navigator.mediaDevices.getUserMedia({ video: true });

        // Mirror Local Video
        localVideo.srcObject = stream;
        localVideo.style.transform = "scaleX(-1)";

        // Add Stream to Peer Connection
        stream.getTracks().forEach(track => pc.addTrack(track, stream));

        // Create Offer & Send SDP
        let offer = await pc.createOffer();
        await pc.setLocalDescription(offer);

        ws.send(JSON.stringify({ sdp: offer.sdp, type: offer.type }));

        // Handle SDP Answer & ICE Candidates
        ws.onmessage = async (event) => {
            let message = JSON.parse(event.data);

            if (message.sdp) {
                await pc.setRemoteDescription(new RTCSessionDescription(message));
                statusMessage.innerText = "✅ Connected to Peer";
            } else if (message.candidate) {
                await pc.addIceCandidate(new RTCIceCandidate(message.candidate));
            }
        };

        // Handle ICE Candidate Events
        pc.onicecandidate = (event) => {
            if (event.candidate) {
                ws.send(JSON.stringify({ candidate: event.candidate }));
            }
        };

        // Set Remote Video Stream
        pc.ontrack = (event) => {
            remoteVideo.srcObject = event.streams[0];
        };

    } catch (error) {
        console.error("Error starting WebRTC:", error);
        statusMessage.innerText = "⚠️ Error Starting Video";
        statusMessage.style.color = "orange";
    }
});
