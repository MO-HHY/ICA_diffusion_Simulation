# UI/UX e Interfaccia del Player

La WebApp disporrà di un layout a griglia fissa per garantire reattività e massima visibilità per i controller del player (Time Travel).

## Wireframe Concettuale

```text
========================================================================================
[HEADER] Healthcare Infection Simulator (HAI) | Scenario: "MRSA Baseline" | [Export CSV]
========================================================================================
[PANNELLO PARAMETRI SCENARIO]  | [VISTA REPARTO (Canvas 2D top-down)]  | [METRICHE LIVE]
-------------------------------|---------------------------------------|----------------
 ▼ AMBIENTE E PATHOGEN         |  +---------+---------+---------+      | [Infezioni] 📈
 Letti: [ 20 ] (10% Isolamento)|  | R_01    | R_02    | R_03    |      |  Casi: 4
 Patogeno: [ MRSA ]            |  |  [P_1🔴]|  [P_2⚪]|  [P_3⚪]|      |  R0 att: 1.2
                               |  |         |         |         |      |----------------
 ▼ STAFF & COMPLIANCE          |  +---_-----+----_----+----_----+      | [Compliance] 📊
 Shift Nurses: [ 4 ]           |      🔵                               |  Target: 60%
 Base Compliance %: [ 60⚙️]    |  [Corridoio Principale]        🟢     |  Reale:  52%
 Efficacia Gel: [ 99% ]        |                                       |----------------
                               |  +---_-----+----_----+----_----+      | [Catena Trans.]
 ▼ AZIONI MACRO                |  | R_04    | R_05    | R_06    |      |
 [⚡ RUN BATCH SIMULATION ]     |  |  [P_4⚪]|  [P_5⚪]|  [EMPTY]|      | > P_1 -> Nurse1
 [📂 LOAD CONFIG ]             |  +---------+---------+---------+      | > Nurse1 -> P_4
========================================================================================
[TIMELINE REPLAY ENGINE]
◀◀ | ⏸️ PAUSE | ▶️ PLAY | x1 - x5 - x20 
Time: Day 1, 14:30 |-----------------🔥-----🧼----------🔥--------------------------|
(Legend keys: 🔥 = Infezione/Spike,  🧼 = Intervento Pulizia Radicale)
========================================================================================
```

### Note Interattive

* I nodi sulle planimetrie sono cliccabili in **Inspect Mode**: Aprendo i tooltip su una stanza o infermiere, vedo lo slider di `Carica ambientale attuale` ed ultimi contatti. Se un paziente è appena divenuto 🔴rosso, un click esporrà la **catena di contagio provata**, permettendo ai direttori d'ospedale di capire retroattivamente l'endpoint di vulnerabilità dei loro turni.
* **Heatmap:** È possibile abilitare l'overlay a gradiente termico (Color scale giallo -> arancio -> rosso scuro) per evincere istantaneamente lo 'sporco batterico e virale' stratificato sulle superfici di appoggio o maniglie che attende lavaggio.
