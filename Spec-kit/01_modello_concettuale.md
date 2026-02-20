# Modello Concettuale: Simulatore HAI

Il sistema è un Multi-Agent Pathfinding Simulator arricchito da dinamiche di diffusione del contagio (modello epidemiologico SIR/ibrido).

## Entità e Stati

1. **Paziente (Nodo statico o semi-statico)**:
   - *Stati Epidemiologici*: (S)uscettibile, (C)olonizzato, (I)nfetto, (R)ecuperato/Dimesso.
   - *Attributi*: `id`, `room_id`, `is_isolated`, `susceptibility_level`, `viral_load` (generazione di patogeno), `los` (length of stay).
   
2. **Staff (Agente Mobile)**: 
   - *Tipi*: Infermiere, Medico, OSS, Addetto alle Pulizie.
   - *Attributi*: `id`, `role`, `hand_contamination_level` (carica patogena trasportata), `base_compliance` (propensione genetica/caratteriale a seguire i protocolli IG), `speed` (velocità di movimento in mappa).
   
3. **Stanza/Ambiente (Serbatoio Spaziale)**:
   - *Attributi*: `id`, `environmental_load` (contaminazione globale delle superfici), `type` (Singola, Doppia, Corridoio, Isolamento, Nursing Station).
   
4. **Patogeno (Regole Logiche)**:
   - Definisce i tassi di trasmissione base, i tempi di emivita (decadimento) sulle mani (minuti) e sulle superfici (ore/giorni).

## Diagramma di Flusso Event-Driven (Tick-based / Event Manager)

Il core engine calcola step o eventi in sequenza logica simulando lo scorrere del tempo:

```text
[Evento: Task di Cura schedulato per Operatore O su Paziente P in Stanza S] 
  |
  +-- 1. Movimento: Pathfinding di O verso S (dalla sua posizione attuale)
  | 
  +-- 2. "Momento 1 OMS" (Prima del contatto):
  |     |-- (Check Compliance): Se test superato -> O effettua lavaggio -> Carica Mani di O diminuisce drasticamente.
  |     |-- Se test fallito -> O ignora il lavaggio -> Carica invariata.
  |
  +-- 3. Interazione / Contatto in Stanza:
  |     |-- O tocca superfici in S: Scambio cross-contaminazione (Superfici S <-> Mani O)
  |     |-- O tocca Paziente P: Scambio cross-contaminazione (Mani O <-> Paziente P)
  |         |-- Se Paziente P = Suscettibile: Calcolo probabilità stocastica di transizione in (C) o (I).
  |         |-- Se Paziente P = Infetto o Colonizzato: Aumento drastico Carica Mani di O e Superfici di S.
  |
  +-- 4. "Momento OMS" (Dopo contatto e uscita):
  |     |-- (Check Compliance): Se test superato -> O effettua lavaggio -> Carica Mani diminuisce.
  |
  +-- 5. Dinamiche Globali continue (ogni tick/ora):
  |     |-- Decadimento biologico: evaporazione carica vitale su superfici/mani (es. log-reduction nel tempo).
  |     +-- Interventi cleaning staff (eventi schedulati): azzerano/riducono fortemente cariche ambientali.
  |
[Fine Evento -> Aggiornamento EventLog -> Fine Tick]
```
