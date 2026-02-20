import simpy
import random
from typing import List, Dict
from datetime import datetime

# L'engine accetta un dizionario validato dal pydantic model in FastAPI
class HAISimulatorEngine:
    def __init__(self, scenario_dict: dict):
        self.scenario = scenario_dict
        
        # Estrai i metadata
        seed = self.scenario["scenario_meta"].get("seed", 42)
        self.max_ticks = self.scenario["simulation"].get("max_ticks", 1000)
        
        # Fissare il random seed garantisce la validazione deterministica del replay
        self.rng = random.Random(seed)
        
        # Inizializza l'ambiente SimPy
        self.env = simpy.Environment()
        
        # Pipeline degli eventi
        self.event_log: List[dict] = []
        
        # Variabili di stato interne (Placeholder prima di fare il mapping completo delle entity)
        self.patients = {}
        self.rooms = {}
        self.staff_agents = []

        # Setup iniziale dal Config
        self._initialize_from_config()

    def _initialize_from_config(self):
        """
        Parsa le liste dal JSON per popolare i node graph (Stanze, Pazienti, Staff).
        """
        # Creiamo un primo log di startup
        self.log_event("START", "Simulation environment initialized", None)
        
        # TODO: Ciclare sui pazienti e referenziare le istanze (PatientEntity)
        # TODO: Inizializzare lo staff e schedulare i loro turni
        pass

    def log_event(self, event_type: str, message: str, tick: float = None):
        """
        Salva la riga evento in EventSourcing (Json lines compatibile)
        """
        t = tick if tick is not None else self.env.now
        log_entry = {
            "t": round(t, 2),
            "type": event_type,
            "msg": message,
            # Possiamo iniettare coordinate, agent_id, target_id ecc in base al tipo
        }
        self.event_log.append(log_entry)

    def agent_process(self, staff_id: str, role: str):
        """
        Il processo generico che guida un agente (Infermiere, OSS) 
        per il loop simpy.Environment.
        """
        while True:
            # 1. Attendi un delta di tempo prima del prossimo task
            yield self.env.timeout(10.0) # Esempio: 10 tick temporali
            
            # 2. Trigger Evento di Contatto / Visita (Momento OMS)
            self.log_event("MOVE", f"{role} {staff_id} moved to random room")
            
            # TODO: Implementare meccanica Cross Contamination e check Compliance Gel Idroalcolico

    def run(self):
        """
        Lancia la simulazione in sincrono fino al max delay configurato
        """
        print(f"Starting simulation for {self.max_ticks} ticks...")
        # Lancia processi fittizi per testare le rotazioni
        for i, config in enumerate(self.scenario.get("staffing", [])):
            role = config["role"]
            for count in range(config["count"]):
                staff_id = f"{role}_{count}"
                # Aggiunge il coroutine-like task al lifecycle SimPy
                self.env.process(self.agent_process(staff_id, role))
        
        # Esecuzione principale bloccante
        self.env.run(until=self.max_ticks)
        
        self.log_event("END", "Simulation Finished", self.env.now)
        return self.event_log
