import simpy
import random
from typing import List, Dict, Optional
from pydantic import BaseModel

# --- Entità Interne del Motore ---

class RoomEntity:
    def __init__(self, room_id: str, r_type: str, env_load: float = 0.0):
        self.id = room_id
        self.type = r_type
        self.load = env_load
        
class PatientEntity:
    def __init__(self, pat_id: str, room_id: str, state: str, susceptibility: float, viral_load: float, is_isolated: bool):
        self.id = pat_id
        self.room_id = room_id
        self.state = state # SUSCEPTIBLE, COLONIZED, INFECTED
        self.susceptibility = susceptibility
        self.load = viral_load
        self.is_isolated = is_isolated

class StaffEntity:
    def __init__(self, staff_id: str, role: str, compliance_mod: float, cleaning_eff: Optional[float]):
        self.id = staff_id
        self.role = role
        self.compliance_modifier = compliance_mod
        self.cleaning_efficacy = cleaning_eff
        self.load = 0.0 # Carica patogena sulle mani


# --- Motore Principale SimPy ---

class HAISimulatorEngine:
    def __init__(self, scenario_dict: dict):
        self.scenario = scenario_dict
        
        # Estrai Metadata
        seed = self.scenario["scenario_meta"].get("seed", 42)
        self.max_ticks = self.scenario["simulation"].get("max_ticks", 1000)
        self.tick_unit_m = self.scenario["simulation"].get("tick_unit_minutes", 10)
        
        # Pathogen details
        p_cfg = self.scenario.get("pathogen", {})
        self.trans_prob = p_cfg.get("transmission_prob", 0.15)
        self.decay_hands = p_cfg.get("decay_hands_half_life_m", 60.0)
        self.decay_surface = p_cfg.get("decay_surface_half_life_h", 72.0)
        
        # Hygiene details
        h_cfg = self.scenario.get("hygiene", {})
        self.base_compliance = h_cfg.get("base_compliance", 0.6)
        self.gel_reduction = h_cfg.get("gel_log_reduction", 0.99)
        self.iso_modifier = h_cfg.get("isolation_modifier", 1.5)

        self.rng = random.Random(seed)
        self.env = simpy.Environment()
        self.event_log: List[dict] = []
        
        # Mappe di stato
        self.rooms: Dict[str, RoomEntity] = {}
        self.patients: Dict[str, PatientEntity] = {}
        self.staff_agents: List[StaffEntity] = []

        self._initialize_from_config()

    def log_event(self, event_type: str, message: str, tick: float = None, **kwargs):
        t = tick if tick is not None else self.env.now
        log_entry = {
            "t": round(t, 2),
            "type": event_type,
            "msg": message,
            **kwargs
        }
        self.event_log.append(log_entry)

    def _initialize_from_config(self):
        """Popola i nodi (Stanze, Pazienti, Staff) validati dal JSON"""
        # 1. Stanze
        hosp = self.scenario.get("hospital", {})
        num_rooms = hosp.get("rooms", 0)
        iso_ids = hosp.get("isolation_ids", [])
        
        for i in range(1, num_rooms + 1):
            rid = f"R_{i:02d}"
            rtype = "ISOLATION" if rid in iso_ids else "SINGLE"
            self.rooms[rid] = RoomEntity(rid, rtype)
            
        # 2. Pazienti
        for p_data in self.scenario.get("patients", []):
            pid = p_data["id"]
            rid = p_data["room"]
            if rid not in self.rooms:
                self.rooms[rid] = RoomEntity(rid, "SINGLE") # Safe fallback fallback
                
            pat = PatientEntity(
                pat_id=pid,
                room_id=rid,
                state=p_data.get("state", "SUSCEPTIBLE"),
                susceptibility=p_data.get("susceptibility", 0.5),
                viral_load=10000.0 if p_data.get("state") in ["INFECTED", "COLONIZED"] else 0.0,
                is_isolated=p_data.get("is_isolated", rid in iso_ids)
            )
            self.patients[pid] = pat
            
        # 3. Staff
        for s_data in self.scenario.get("staffing", []):
            role = s_data["role"]
            for i in range(s_data.get("count", 1)):
                sid = f"{role}_{i+1}"
                staff = StaffEntity(
                    staff_id=sid,
                    role=role,
                    compliance_mod=s_data.get("compliance_modifier", 1.0),
                    cleaning_eff=s_data.get("cleaning_efficacy", None)
                )
                self.staff_agents.append(staff)

        self.log_event("START", "Simulation environment initialized")

    def _decay_process(self):
        """Processo globale continuo che riduce le cariche virali basato sull'emivita"""
        while True:
            yield self.env.timeout(1.0) # Ogni tick (~10 minuti simulati)
            
            # Decadimento Superfici (Emivita in ore, quindi in tick = HalfLifeH * 60 / TickM)
            # Formula semplificata per diminuzione logaritmica a scalini
            surface_decay_factor = 1.0 - (0.693 / (self.decay_surface * 60.0 / self.tick_unit_m))
            for r in self.rooms.values():
                if r.load > 0.01:
                    r.load *= max(0, surface_decay_factor)

            # Decadimento Mani
            hands_decay_factor = 1.0 - (0.693 / (self.decay_hands / self.tick_unit_m))
            for s in self.staff_agents:
                if s.load > 0.01:
                    s.load *= max(0, hands_decay_factor)

    def _hand_hygiene_check(self, agent: StaffEntity, room: RoomEntity) -> bool:
        """Calcola stocasticamente se l'agente esegue l'igiene delle mani."""
        target_prob = self.base_compliance * agent.compliance_modifier
        if room.type == "ISOLATION":
            target_prob *= self.iso_modifier
        
        target_prob = min(target_prob, 0.99) # max 99% cap
        
        if self.rng.random() < target_prob:
            # Successo: abbattimento carica mani
            agent.load *= (1.0 - self.gel_reduction)
            return True
        return False

    def _cross_contaminate(self, agent: StaffEntity, room: RoomEntity, patient: PatientEntity = None):
        """Meccanica di scambio carica virale e innesco infezioni"""
        
        # 1. Contatto Ambiente <-> Mani
        room_pickup = room.load * 0.10 # Il 10% della carica della stanza finisce sulle mani
        hands_drop = agent.load * 0.05 # Il 5% delle mani resta nella stanza
        
        agent.load = agent.load + room_pickup - hands_drop
        room.load = room.load + hands_drop - room_pickup
        
        # 2. Contatto Paziente <-> Mani
        if patient:
            pat_pickup = patient.load * 0.15
            pat_drop = agent.load * 0.10
            
            agent.load = agent.load + pat_pickup - pat_drop
            patient.load = patient.load + pat_drop - pat_pickup
            
            # 3. Check Infezione (Suscettibile -> Colonizzato)
            if patient.state == "SUSCEPTIBLE" and pat_drop > 10.0:
                # La probabilità di infettarsi dipende dalla carica caduta e dalla prob base
                infection_risk = min(1.0, (pat_drop / 1000.0) * self.trans_prob * patient.susceptibility)
                if self.rng.random() < infection_risk:
                    patient.state = "INFECTED"
                    patient.load = 10000.0 # Raggiunge cap virale
                    self.log_event("INFECTION", f"Patient {patient.id} infected by {agent.id}", 
                                   source=agent.id, target=patient.id, mechanism="DIRECT_HANDS")

    def agent_process(self, agent: StaffEntity):
        """Il ciclo vita (Turno) di un operatore nel reparto."""
        room_ids = list(self.rooms.keys())
        
        while True:
            # Delay fino al prossimo task (1-3 tick / 10-30 min)
            yield self.env.timeout(self.rng.randint(1, 3))
            
            # Sceglie una stanza a caso da visitare
            target_room_id = self.rng.choice(room_ids)
            target_room = self.rooms[target_room_id]
            
            # Cerca se c'è un paziente
            target_patient = next((p for p in self.patients.values() if p.room_id == target_room_id), None)
            
            self.log_event("MOVE", f"{agent.role} {agent.id} visiting {target_room_id}", agent_id=agent.id, room=target_room_id)
            
            # CLEANER LOGIC: Pulizia
            if agent.role == "CLEANER":
                target_room.load *= (1.0 - (agent.cleaning_efficacy or 0.85))
                self.log_event("CLEANING", f"{agent.id} cleaned {target_room_id}", agent_id=agent.id, room=target_room_id)
                continue
                
            # NURSE/DOC LOGIC: Visita Clinica
            # Momento OMS 1: Prima del contatto (Ingresso)
            if self._hand_hygiene_check(agent, target_room):
                self.log_event("HYGIENE", "WASH_IN_SUCCESS", agent_id=agent.id, room=target_room_id)
            else:
                self.log_event("HYGIENE", "WASH_IN_FAIL", agent_id=agent.id, room=target_room_id)
                
            # Interazione (Cross-Contaminazione)
            self._cross_contaminate(agent, target_room, target_patient)
            
            # Momento OMS 2: Dopo il contatto (Uscita)
            if self._hand_hygiene_check(agent, target_room):
                self.log_event("HYGIENE", "WASH_OUT_SUCCESS", agent_id=agent.id, room=target_room_id)
            else:
                self.log_event("HYGIENE", "WASH_OUT_FAIL", agent_id=agent.id, room=target_room_id)

    def run(self) -> List[dict]:
        """Esegue il calcolo della run."""
        print(f"[SimPy Engine] Starting scenario '{self.scenario['scenario_meta']['name']}' for {self.max_ticks} ticks...")
        
        # Schedula Decadimento Ambientale
        self.env.process(self._decay_process())
        
        # Schedula Agenti
        for staff in self.staff_agents:
            self.env.process(self.agent_process(staff))
        
        # Avvia Clock
        self.env.run(until=self.max_ticks)
        
        self.log_event("END", "Simulation Finished")
        return self.event_log
