from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI(title="HAI Simulator API", version="0.1.0")

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = None
db = None

@app.on_event("startup")
async def startup_db_client():
    global client, db
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.hai_simulator
    print(f"Connected to MongoDB at {MONGO_URL}")

@app.on_event("shutdown")
async def shutdown_db_client():
    if client:
        client.close()

@app.get("/")
async def root():
    return {"message": "HAI Simulator API is running"}

@app.get("/health")
async def health_check():
    # Controllo stato connessione al database
    try:
        await db.command("ping")
        db_status = "ok"
    except Exception as e:
        db_status = str(e)
    return {"status": "healthy", "database": db_status}
