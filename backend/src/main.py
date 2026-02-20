from fastapi import FastAPI, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
import os
from contextlib import asynccontextmanager
from bson import ObjectId

# Importiamo i modelli definiti (usando path relativo dal package engine)
from .engine.models import ScenarioInput

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = None
db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, db
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.hai_simulator
    print(f"Connected to MongoDB at {MONGO_URL}")
    yield
    if client:
        client.close()

app = FastAPI(title="HAI Simulator API", version="0.1.0", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "HAI Simulator API is running"}

@app.get("/health")
async def health_check():
    try:
        await db.command("ping")
        db_status = "ok"
    except Exception as e:
        db_status = str(e)
    return {"status": "healthy", "database": db_status}

# CRUD Endpoint per gli Scenari
@app.post("/scenarios", status_code=status.HTTP_201_CREATED)
async def create_scenario(scenario: ScenarioInput):
    """
    Riceve un JSON Scenario, lo valida tramita Pydantic 
    e lo salva su MongoDB nella collection `scenarios`.
    """
    scenario_dict = scenario.model_dump()
    result = await db.scenarios.insert_one(scenario_dict)
    return {"id": str(result.inserted_id), "message": "Scenario created successfully"}

@app.get("/scenarios")
async def list_scenarios():
    """
    Ritorna la lista degli scenari salvati con il loro nome e descrizione.
    """
    scenarios = []
    cursor = db.scenarios.find({}, {"scenario_meta": 1})
    async for doc in cursor:
        scenarios.append({
            "id": str(doc["_id"]),
            "name": doc["scenario_meta"].get("name"),
            "description": doc["scenario_meta"].get("description")
        })
    return scenarios

@app.get("/scenarios/{scenario_id}")
async def get_scenario(scenario_id: str):
    """
    Restituisce il dettaglio completo di uno scenario tramite ID.
    """
    if not ObjectId.is_valid(scenario_id):
         raise HTTPException(status_code=400, detail="Invalid ID format")
    
    doc = await db.scenarios.find_one({"_id": ObjectId(scenario_id)})
    if doc is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    doc["id"] = str(doc.pop("_id"))
    return doc

@app.post("/scenarios/{scenario_id}/run")
async def run_simulation(scenario_id: str):
    """
    [WIP] Innesca l'engine SimPy per lo scenario richiesto.
    Al momento è un Placeholder.
    """
    # 1. Recupero scenario
    # 2. Passo il dict all'engine Simpy
    # 3. Restituisco l'ID della run che si sta eseguendo (async worker)
    return {"message": f"Simulation initiated for scenario {scenario_id}", "run_id": "placeholder_run"}
