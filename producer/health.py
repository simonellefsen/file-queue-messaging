from fastapi import FastAPI

health_app = FastAPI()

@health_app.get("/live")
async def liveness():
    return {"status": "alive"}

@health_app.get("/ready")
async def readiness():
    return {"status": "ready"}

