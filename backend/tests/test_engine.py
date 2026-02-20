import os
import sys

# Aggiungiamo il parent folder al sys.path per importare `src`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine.simulator import HAISimulatorEngine
from src.engine.models import ScenarioInput

def get_base_scenario():
    return {
      "scenario_meta": { "name": "Test Scenario", "seed": 42 },
      "hospital": { "rooms": 2, "isolation_ids": ["R_01"] },
      "staffing": [
        { "role": "NURSE", "count": 1, "compliance_modifier": 1.0 },
        { "role": "CLEANER", "count": 1, "cleaning_efficacy": 0.85 }
      ],
      "patients": [
        { "id": "P_INDEX", "room": "R_01", "state": "INFECTED", "susceptibility": 1.0 },
        { "id": "P_001", "room": "R_02", "state": "SUSCEPTIBLE", "susceptibility": 0.9 }
      ],
      "pathogen": {
        "type": "MRSA", "transmission_prob": 0.5, "decay_surface_half_life_h": 72
      },
      "hygiene": {
        "base_compliance": 0.5, "gel_log_reduction": 0.99
      },
      "simulation": { "max_ticks": 50, "tick_unit_minutes": 10 }
    }

def test_engine_determinism():
    """ Verifica il Determinismo Stocastico (Replay Assoluto) garantito dal seed """
    scenario = get_base_scenario()
    
    # Esecuzione 1
    engine_1 = HAISimulatorEngine(scenario)
    log_1 = engine_1.run()
    
    # Esecuzione 2
    engine_2 = HAISimulatorEngine(scenario)
    log_2 = engine_2.run()

    # Le run devono durare lo stesso e produrre gli esatti eventi
    assert len(log_1) == len(log_2), "Le due simulazioni hanno generato log di lunghezza diversa"
    
    for e1, e2 in zip(log_1, log_2):
        assert e1["t"] == e2["t"], f"Delay temporale stocastico fallito: {e1} vs {e2}"
        assert e1["type"] == e2["type"], f"Tipo evento stocastico divergente: {e1} vs {e2}"

def test_hygiene_success_rate():
    """ 
    Se mettiamo la compliance molto alta o bassa, gli hint statistici
    sui log degli eventi devono riflettere i parametri config.
    """
    scenario = get_base_scenario()
    
    # Forziamo compliance 100%
    scenario["hygiene"]["base_compliance"] = 1.0
    scenario["staffing"][0]["compliance_modifier"] = 1.0
    engine_high = HAISimulatorEngine(scenario)
    log_high = engine_high.run()
    
    fails_high = sum(1 for e in log_high if e.get("msg") in ["WASH_IN_FAIL", "WASH_OUT_FAIL"])
    assert fails_high <= sum(1 for e in log_high if e.get("type") == "HYGIENE") * 0.1 # < 10% fallimenti (o addirittura 0%)
    
    # Forziamo compliance 0%
    scenario["hygiene"]["base_compliance"] = 0.0
    engine_low = HAISimulatorEngine(scenario)
    log_low = engine_low.run()
    
    success_low = sum(1 for e in log_low if e.get("msg") in ["WASH_IN_SUCCESS", "WASH_OUT_SUCCESS"])
    assert success_low == 0 # 0 successi
