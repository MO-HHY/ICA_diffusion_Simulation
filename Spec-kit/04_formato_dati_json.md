# Specifiche JSON: Formato Dati e I/O

Il sistema prevede una netta divisione Architetturale tra l'Input (Configurazione dello "**Scenario**") e l'Output (Registro log per Data viz / replaying "**EventLog**").

## 1. Scenario / Input (JSON)

Rappresenta lo stato 0 del sistema, e i setup statici.

```json
{
  "scenario_meta": { 
    "name": "MRSA_LowStaff_HighCompliance", 
    "seed": 42 
  },
  "hospital": {
    "rooms": 12,
    "isolation_ids": ["R_01", "R_02"]
  },
  "staffing": [
    { "role": "NURSE", "count": 4, "compliance_modifier": 1.0 },
    { "role": "DOC", "count": 1, "compliance_modifier": 0.8 },
    { "role": "CLEANER", "count": 1, "cleaning_efficacy": 0.85 }
  ],
  "patients": [
    { "id": "P_INDEX", "room": "R_01", "state": "INFECTED", "susceptibility": 1.0 },
    { "id": "P_002", "room": "R_02", "state": "SUSCEPTIBLE", "susceptibility": 0.5 }
  ],
  "pathogen": {
    "type": "MRSA",
    "transmission_prob": 0.15,
    "decay_surface_half_life_h": 72
  }
}
```

## 2. EventLog / Output (JSON Lines)

Il paradigma è l'`Event-Sourcing`, ossia append-only stream cronologico.
Questo log testuale permette al Frontend di riprodurre animazioni 2D pixel per pixel senza chiamare il backend, agendo come "Replay Player" staccato.

```jsonlines
{"t": 0.0, "type": "START", "msg": "Simulation started"}
{"t": 1.2, "type": "MOVE", "agent": "NURSE_1", "destination": "R_01"}
{"t": 1.4, "type": "HYGIENE", "agent": "NURSE_1", "action": "WASH", "result": "FAIL"}
{"t": 1.5, "type": "CONTACT", "agent": "NURSE_1", "target_type": "ENV", "target": "R_01", "agent_load_after": 500}
{"t": 1.6, "type": "CONTACT", "agent": "NURSE_1", "target_type": "PAT", "target": "P_INDEX", "agent_load_after": 2500}
{"t": 3.1, "type": "INFECTION", "source": "NURSE_1", "target": "P_002", "mechanism": "DIRECT_CONTACT_HANDS"}
```
