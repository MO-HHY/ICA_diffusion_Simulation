from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class RoomConfig(BaseModel):
    id: str
    type: Literal["SINGLE", "DOUBLE", "CORRIDOR", "ISOLATION", "NURSING_STATION"] = "SINGLE"
    environmental_load: float = 0.0

class PatientConfig(BaseModel):
    id: str
    room: str
    state: Literal["SUSCEPTIBLE", "COLONIZED", "INFECTED", "RECOVERED"] = "SUSCEPTIBLE"
    susceptibility: float = Field(default=0.5, ge=0.0, le=1.0)
    viral_load: float = 0.0
    is_isolated: bool = False

class StaffConfig(BaseModel):
    role: Literal["NURSE", "DOC", "CLEANER", "OSS"]
    count: int = 1
    compliance_modifier: float = 1.0
    cleaning_efficacy: Optional[float] = None

class PathogenConfig(BaseModel):
    type: str = "MRSA"
    transmission_prob: float = Field(default=0.15, ge=0.0, le=1.0)
    decay_surface_half_life_h: float = 72.0
    decay_hands_half_life_m: float = 60.0

class HygieneConfig(BaseModel):
    base_compliance: float = Field(default=0.6, ge=0.0, le=1.0)
    isolation_modifier: float = 1.5
    gel_log_reduction: float = 0.99

class SimulationConfig(BaseModel):
    max_ticks: int = 1000
    tick_unit_minutes: int = 10

class ScenarioMeta(BaseModel):
    name: str
    seed: int = 42
    description: str = ""

class HospitalConfig(BaseModel):
    rooms: int
    isolation_ids: List[str] = []

class ScenarioInput(BaseModel):
    """
    Main Pydantic model representing the Input JSON Scenario.
    """
    scenario_meta: ScenarioMeta
    hospital: HospitalConfig
    staffing: List[StaffConfig]
    patients: List[PatientConfig]
    pathogen: PathogenConfig
    hygiene: HygieneConfig
    simulation: SimulationConfig
