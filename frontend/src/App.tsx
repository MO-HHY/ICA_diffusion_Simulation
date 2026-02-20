import { useState, useEffect } from 'react';
import axios from 'axios';
import { Play, Activity, FolderOpen, ShieldAlert } from 'lucide-react';
import SimulationViewer from './components/SimulationViewer';
import './index.css';

const API_BASE = 'http://localhost:8080';

// Tipi Base
interface ScenarioMeta {
  id: string;
  name: string;
  description: string;
}

interface RunLog {
  id: string;
  scenario_id: string;
  timestamp: string;
  ticks_simulated: number;
  event_log_size: number;
  events: any[];
}

function App() {
  const [scenarios, setScenarios] = useState<ScenarioMeta[]>([]);
  const [selectedScenario, setSelectedScenario] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeRun, setActiveRun] = useState<RunLog | null>(null);

  useEffect(() => {
    fetchScenarios();
  }, []);

  const fetchScenarios = async () => {
    try {
      const resp = await axios.get(`${API_BASE}/scenarios`);
      setScenarios(resp.data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleRunSimulation = async () => {
    if (!selectedScenario) return;
    setLoading(true);
    try {
      // 1. Trigger la Run
      const runResp = await axios.post(`${API_BASE}/scenarios/${selectedScenario}/run`);
      const runId = runResp.data.run_id;

      // 2. Fetch i risultati
      const dataResp = await axios.get(`${API_BASE}/runs/${runId}`);
      setActiveRun(dataResp.data);
    } catch (e) {
      console.error(e);
      alert("Errore nell'esecuzione della simulazione!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto', width: '100%' }}>
      <header style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
        <ShieldAlert size={40} color="#3b82f6" />
        <div>
          <h1 style={{ margin: 0, fontSize: '2rem' }}>HAI Simulator</h1>
          <p style={{ margin: 0, color: '#94a3b8' }}>Healthcare-Associated Infections Engine</p>
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>

        {/* Sinistra: Scenari */}
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.25rem' }}>
            <FolderOpen size={20} /> Scenari Disponibili
          </h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1.5rem' }}>
            {scenarios.map(s => (
              <div
                key={s.id}
                onClick={() => setSelectedScenario(s.id)}
                style={{
                  padding: '1rem',
                  borderRadius: '8px',
                  background: selectedScenario === s.id ? 'rgba(59, 130, 246, 0.2)' : 'rgba(255,255,255,0.05)',
                  border: `1px solid ${selectedScenario === s.id ? '#3b82f6' : 'transparent'}`,
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
              >
                <div style={{ fontWeight: 600 }}>{s.name}</div>
                <div style={{ fontSize: '0.875rem', color: '#94a3b8', marginTop: '0.25rem' }}>
                  {s.description || 'Nessuna descrizione.'}
                </div>
              </div>
            ))}
            {scenarios.length === 0 && (
              <div style={{ color: '#94a3b8', fontStyle: 'italic' }}>
                Nessuno scenario presente nel Database. Usa le API per caricarne uno.
              </div>
            )}
          </div>

          <button
            className="btn"
            style={{ width: '100%', marginTop: '2rem', justifyContent: 'center' }}
            disabled={!selectedScenario || loading}
            onClick={handleRunSimulation}
          >
            {loading ? <Activity className="infected-pulse" /> : <Play />}
            {loading ? 'Simulazione in corso...' : 'Avvia Simulazione'}
          </button>
        </div>

        {/* Destra: Risultati e Viewer */}
        <div className="glass-panel" style={{ padding: '1.5rem', minHeight: '600px' }}>
          {activeRun ? (
            <div>
              <h2 style={{ color: '#10b981' }}>✔️ Simulazione Completata! (ID: {activeRun.id})</h2>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginTop: '1.5rem' }}>
                <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '8px' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Ticks Simulati</div>
                  <div style={{ fontSize: '1.5rem', fontWeight: 600 }}>{activeRun.ticks_simulated}</div>
                </div>
                <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '8px' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Punti Evento (EventSourcing)</div>
                  <div style={{ fontSize: '1.5rem', fontWeight: 600 }}>{activeRun.event_log_size}</div>
                </div>
                <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '8px' }}>
                  <div style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Timestamp</div>
                  <div style={{ fontSize: '1rem', fontWeight: 600, marginTop: '0.5rem' }}>{new Date().toLocaleTimeString()}</div>
                </div>
              </div>

              <div style={{ marginTop: '2rem', padding: '2rem', border: '1px dashed rgba(255,255,255,0.2)', borderRadius: '12px', textAlign: 'center' }}>
                <Activity size={48} color="#94a3b8" style={{ marginBottom: '1rem', display: 'inline-block' }} />
                <h3>Canvas EventSourcing Viewer 2D</h3>
                <p style={{ color: '#94a3b8', marginBottom: '2rem' }}>
                  Animazione in base agli eventi stocastici di spostamento e infezione elaborati dal motore SimPy.
                </p>
                <div style={{ textAlign: 'left' }}>
                  <SimulationViewer events={activeRun.events} maxTicks={activeRun.ticks_simulated} />
                </div>
              </div>

            </div>
          ) : (
            <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: '#94a3b8' }}>
              <Activity size={64} style={{ opacity: 0.2, marginBottom: '1rem' }} />
              <p>Seleziona uno Scenario a sinistra ed avvia il simulatore stocastico per vedere i risultati.</p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}

export default App;
