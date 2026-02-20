import React, { useEffect, useRef, useState } from 'react';
import { Play, Pause } from 'lucide-react';

interface SimulationViewerProps {
    events: any[];
    maxTicks: number;
}

// Coordinate Fittizie Struttura Ospedale (Layout Base)
const ROOM_LAYOUT: Record<string, { x: number, y: number, w: number, h: number, name: string }> = {
    "R_01": { x: 50, y: 50, w: 200, h: 150, name: "Stanza 1 (Isolamento)" },
    "R_02": { x: 300, y: 50, w: 200, h: 150, name: "Stanza 2" },
    "CORRIDOR": { x: 50, y: 200, w: 700, h: 80, name: "Corridoio Principale" },
};

const SimulationViewer: React.FC<SimulationViewerProps> = ({ events, maxTicks }) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [currentTick, setCurrentTick] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);
    const [playbackSpeed, setPlaybackSpeed] = useState(500); // ms per tick in auto-play

    // Costruzione dello stato aggregato fotogramma per fotogramma
    // In produzione si farebbe un reducer, qui calcoliamo lo snapshot al volo per l'MVP
    const getSnapshotAtTick = (tick: number) => {
        const state = {
            patients: {} as Record<string, { room: string, state: string }>,
            staff: {} as Record<string, { room: string }>,
            rooms: { "R_01": 0, "R_02": 0 } as Record<string, number> // viral load base
        };

        // replay events up to 'tick'
        events.filter(e => e.t <= tick).forEach(e => {
            if (e.type === "MOVE") {
                state.staff[e.agent_id] = { room: e.room };
            }
            if (e.type === "INFECTION") {
                // Aggiorniamo stato paziente
                state.patients[e.target] = { ...state.patients[e.target], state: "INFECTED" };
            }
        });

        // Dummy initial state se non specificato
        if (!state.patients["P_INDEX"]) state.patients["P_INDEX"] = { room: "R_01", state: "INFECTED" };
        if (!state.patients["P_001"]) state.patients["P_001"] = { room: "R_02", state: "SUSCEPTIBLE" };

        return state;
    };

    useEffect(() => {
        let interval: any;
        if (isPlaying) {
            interval = setInterval(() => {
                setCurrentTick(prev => {
                    if (prev >= maxTicks) {
                        setIsPlaying(false);
                        return prev;
                    }
                    return prev + 1;
                });
            }, playbackSpeed);
        }
        return () => clearInterval(interval);
    }, [isPlaying, playbackSpeed, maxTicks]);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // Sfondo Dark
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const snapshot = getSnapshotAtTick(currentTick);

        // Disegna Stanze
        Object.values(ROOM_LAYOUT).forEach((r) => {
            // Background stanza (Leggermente più chiaro + bordo)
            ctx.fillStyle = '#1e293b';
            ctx.strokeStyle = '#334155';
            ctx.lineWidth = 2;
            ctx.fillRect(r.x, r.y, r.w, r.h);
            ctx.strokeRect(r.x, r.y, r.w, r.h);

            // Label
            ctx.fillStyle = '#94a3b8';
            ctx.font = '12px Inter';
            ctx.fillText(r.name, r.x + 10, r.y + 20);
        });

        // Disegna Pazienti
        // Per semplicità posizioniamo il paziente al centro della sua stanza
        Object.entries(snapshot.patients).forEach(([pId, pData]) => {
            const room = ROOM_LAYOUT[pData.room];
            if (!room) return;

            const px = room.x + room.w / 2;
            const py = room.y + room.h / 2;

            ctx.beginPath();
            ctx.arc(px, py, 15, 0, 2 * Math.PI);

            // Suscettibile = Blu, Infetto = Rosso
            ctx.fillStyle = pData.state === 'INFECTED' ? '#ef4444' : '#3b82f6';
            ctx.fill();
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.stroke();

            ctx.fillStyle = '#fff';
            ctx.font = '10px Inter';
            ctx.fillText(pId, px - 12, py + 25);
        });

        // Disegna Staff
        // Offset per non sovrapporsi col paziente
        const staffOffsets = [{ dx: -30, dy: -30 }, { dx: 30, dy: 30 }, { dx: -30, dy: 30 }, { dx: 30, dy: -30 }];
        let sIdx = 0;
        Object.entries(snapshot.staff).forEach(([sId, sData]) => {
            let rx = 50, ry = 240; // Default in corridoio
            const targetRoom = ROOM_LAYOUT[sData.room];
            if (targetRoom) {
                const off = staffOffsets[sIdx % staffOffsets.length];
                rx = targetRoom.x + targetRoom.w / 2 + off.dx;
                ry = targetRoom.y + targetRoom.h / 2 + off.dy;
                sIdx++;
            }

            ctx.beginPath();
            ctx.arc(rx, ry, 10, 0, 2 * Math.PI);

            // Staff = Verde
            ctx.fillStyle = '#10b981';
            ctx.fill();

            ctx.fillStyle = '#10b981';
            ctx.font = '10px Inter';
            ctx.fillText(sId, rx - 15, ry - 15);
        });

    }, [currentTick, events, maxTicks]);

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>

            {/* Controlli Player */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '8px' }}>
                <button className="btn" style={{ padding: '0.5rem' }} onClick={() => setIsPlaying(!isPlaying)}>
                    {isPlaying ? <Pause size={20} /> : <Play size={20} />}
                </button>

                <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <span style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Tick: {currentTick} / {maxTicks}</span>
                    <input
                        type="range"
                        min="0" max={maxTicks}
                        value={currentTick}
                        onChange={(e) => { setIsPlaying(false); setCurrentTick(Number(e.target.value)); }}
                        style={{ flex: 1, cursor: 'pointer' }}
                    />
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span style={{ fontSize: '0.875rem', color: '#94a3b8' }}>Velocità:</span>
                    <select
                        value={playbackSpeed}
                        onChange={e => setPlaybackSpeed(Number(e.target.value))}
                        style={{ background: '#1e293b', color: 'white', border: '1px solid #334155', borderRadius: '4px', padding: '0.25rem' }}
                    >
                        <option value="1000">1x (Lenta)</option>
                        <option value="500">2x (Normale)</option>
                        <option value="100">5x (Veloce)</option>
                        <option value="10">Max</option>
                    </select>
                </div>
            </div>

            <div style={{ overflowX: 'auto', background: '#020617', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.1)' }}>
                <canvas
                    ref={canvasRef}
                    width={800}
                    height={400}
                    style={{ display: 'block', margin: '0 auto' }}
                />
            </div>

        </div>
    );
};

export default SimulationViewer;
