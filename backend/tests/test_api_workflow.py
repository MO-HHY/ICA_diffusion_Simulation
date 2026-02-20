import json
import time
import urllib.request
import urllib.error

API_URL = "http://localhost:8080"
SCENARIO_PATH = "Spec-kit/examples/scenario_minimale.json"

def test_api_workflow():
    print("--- 1. Testing API Health ---")
    try:
        req = urllib.request.Request(f"{API_URL}/health")
        with urllib.request.urlopen(req) as resp:
            print(json.loads(resp.read().decode()))
    except Exception as e:
        print(f"API Health error: {e}")
        return

    print("\n--- 2. Uploading Scenario Minimal ---")
    with open(SCENARIO_PATH, "r") as f:
        payload = f.read().encode('utf-8')
    
    req = urllib.request.Request(f"{API_URL}/scenarios", data=payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as resp:
            created = json.loads(resp.read().decode())
            s_id = created["id"]
            print(f"Success! Scenario ID: {s_id}")
    except urllib.error.HTTPError as e:
        print(f"Error creating scenario: {e.read().decode()}")
        return

    print("\n--- 3. Running Simulation ---")
    start = time.time()
    req_run = urllib.request.Request(f"{API_URL}/scenarios/{s_id}/run", method="POST")
    try:
        with urllib.request.urlopen(req_run) as resp:
            duration = time.time() - start
            run_res = json.loads(resp.read().decode())
            print(f"Simulazione Finita in {duration:.2f}s!")
            print(f"Run ID MongoDB: {run_res.get('run_id')}")
            print(f"Eventi Generati: {run_res.get('total_events')}")
    except urllib.error.HTTPError as e:
        print(f"Error running simulation: {e.read().decode()}")

if __name__ == "__main__":
    test_api_workflow()
