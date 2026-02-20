# Architettura Tecnica e Algoritmo di Simulazione

## Definizione Stack Architetturale

- **Backend Orchestrator & API**: **FastAPI** (Python 3.10+) in container Docker. Fornisce le REST API per gestire esperimenti e parametri dalla UI.
- **Core Engine**: Integrato nell'API Python, usa `SimPy` per il calcolo discrete-event simulation. Garantisce le performance tramite routine pre-compilate internamente a Python.
- **Database Storage**: **MongoDB** (in container dedicato via Docker Compose). Memorizza staticamente i JSON degli scenari creati, i meta-dati delle "Simulation Runs" e ospita l'`EventLog` in documenti (o ne indicizza il path su disco) in modo nativo.
- **Frontend / UI**: Applicazione separata web React/Vite + Canvas. Interroga le REST API FastAPI per scaricare lo stream temporale e animare il riproduttore.

## Configurazione di una Run

L'engine legge il file di scenario (`.json`) che descrive: struttura planimetrica, agenti (staff e pazienti con seed iniziale di contagio) e le regole temporali (Compliance e Patogeno).
Emette in pipe log serializzati passo-passo o logga a blocchi in file append-only preposti.

## Algoritmo Engine: Pseudo-Codice (Simulazione Discreta)

```python
import random, heapq

class SimulatorEngine:
    def __init__(self, scenario_config, seed=42):
        self.rng = random.Random(seed) # Random seed fissato per garanzia di replicabilità dei replay
        self.time = 0
        self.state = initialize_hospital(scenario_config)
        self.event_queue = [] # Priority queue cronologica (min-heap su tempo di evento)
        self.log = []
    
    def process_contact(self, agent, target, target_type, time):
        """ Calcola la cross-contaminazione differenziale e probabilistiche d'infezione. """
        # Contaminazione incrociata vettoriale: Mani <-> Paziente / Superficie
        transfer_agent_to_target = agent.load * transmission_rate(target_type)
        transfer_target_to_agent = target.load * pickup_rate(target_type)
        
        agent.load += transfer_target_to_agent
        target.load += transfer_agent_to_target
        
        # Meccanismo di Trasmissione (S -> C/I)
        if target_type == "PATIENT" and target.state == "SUSCEPTIBLE":
            infection_chance = (agent.load / INFECTION_THRESHOLD) * target.susceptibility
            if self.rng.random() < infection_chance:
                target.state = "COLONIZED"
                # Evento fondamentale in Log
                self.log_event("INFECTION", time=time, source=agent.id, target=target.id, reason="DIRECT_CONTACT")

    def run_simulation(self, max_ticks):
        while self.event_queue and self.time < max_ticks:
            event = heapq.heappop(self.event_queue)
            
            # Applica decadimento biologico ambientale sul tempo intercorso dall'ultimo check stanza
            apply_environmental_decay(delta_time=event.time - self.time)
            self.time = event.time
            
            if event.type == "TASK_PATIENT":
                # Step 1: Momento 1 OMS (Prima isolamento/paziente)
                compliance_prob = get_compliance(event.agent, event.room)
                if self.rng.random() < compliance_prob:
                    event.agent.load *= (1.0 - GEL_REDUCTION)
                    self.log_event("HYGIENE_SUCCESS", agent=event.agent.id, time=self.time)
                else:
                    self.log_event("HYGIENE_FAIL", agent=event.agent.id, time=self.time)

                # Step 2: Interazioni Stanza
                self.process_contact(event.agent, event.patient, "PATIENT", self.time)
                self.process_contact(event.agent, event.room, "ENVIRONMENT", self.time)
```
