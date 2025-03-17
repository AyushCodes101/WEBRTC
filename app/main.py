from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.stream_routes import router
from app.config.logger import logger

app = FastAPI() 

app.include_router(router)
app.mount("/static", StaticFiles(directory="frontend/assets"), name="static")

@app.get("/")
def root():
    return {"message": "WebRTC Streaming Server Running"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting WebRTC Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)