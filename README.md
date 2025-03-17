# WebRTC Live Video Streaming 🚀

This project enables real-time video streaming using **WebRTC** with a **FastAPI WebSocket server**.  
Users can start a live video stream and connect to peers using a browser.

---

## 📌 Features
✅ **Live Video Streaming** between peers.  
✅ **WebSocket-based Signaling** for SDP and ICE exchange.  
✅ **Connection Status Messages** (Connected, Disconnected, Error).  
✅ **Mirrored Local Video** (Fixes flipped webcam issue).  
✅ **Automatic ICE Candidate Handling** for WebRTC.  
✅ **Modular & Clean Code** with error handling.  

---

## 📁 Folder Structure

/project-root │── /app (Backend API)
                 │── /assets (CSS, Images)  
                    │── /scripts (JS Files) 
                        │── /templates (HTML Files) 
                            │── main.py (FastAPI WebSocket Server) │── README.md


---

## 🚀 Installation & Setup

### **1️⃣ Install Dependencies**
Make sure you have **Python 3.8+** installed.

```sh
pip install fastapi uvicorn
