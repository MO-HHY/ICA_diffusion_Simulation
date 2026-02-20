# Backlog di Sviluppo (MVP → V1)

L'adozione di un approccio Agile permetterà validazioni progressive del tool, partendo dal core matematico per terminare alla UI.

## Sprint 1: MVP Core Logic (Settimane 1-2)

- **US-1.1**: *Come backend dev, voglio uno script base `engine.py` (SimPy) che preleva istanze da JSON e fa muovere 2 agenti nurse su 5 stanze in random-walk ma in maniera ordinata come task schedulati.*
- **US-1.2**: *Come epidemiologo, voglio un placeholder della classe `Pathogen` e applicare le formule logaritmiche di decadimento temporale sulle mani (15~60 min).*
- **US-1.3**: *Come utente, voglio che un paziente "Infetto Iniziale" trasferisca una proporzione del suo carico di virulenza sull'agent-mani in caso di non lavaggio post-visita.*
- **US-1.4**: *Come frontend dev, voglio un viewer HTML/Canvas base in locale che interpola uno stream/file testuale statico `EventLog.jsonl` solo per muovere i pallini nelle rispettive aree.*

## Sprint 2: MVP Features & Data Viewer (Settimane 2-3)

- **US-2.1**: *Come utente, voglio vedere nel pannello di destra il Line Chart Recharts.js che si aggiorna in tempo reale col conteggio aggiornato dei cluster Infetti/Suscettibili nel tempo della simulazione.*
- **US-2.2**: *Come utente, voglio i bottoni operativi del Replayer Eventi: `Play, Pause, Speedx5` collegati alla progress bar o timeline.*
- **US-2.3 (Validazione testuale)**: *Test di integrità: Settando 100% compliance da file json, l'engine processa 0 "INFECTION" logs per tutto il ciclo operativo del reparto confermando null risk transmission.*

*(Milestone: Rilascio MVP Interno: Core Simulation visualmente verificabile e reattiva ai parametri).*

## Sprint 3-4: V1 "Environmental Modeling" (Settimane 4-6)

- **US-3.1**: *Come scienziato dei dati, voglio splittare vettore mani dal vettore aria/fomiti: gli operatori diffondono virulenza sulle stanze ad ogni ingresso e questa persiste influenzando altri agent.*
- **US-3.2**: *Come utente finale, voglio poter switchare il toggle mappa reparto su `Heatmap Contamination Mode`, così che una stanza con scarso arieggiamento e pulizie mostri alone rosso acceso.*
- **US-3.3**: *Come manager ospedaliero ricalibrando turni, voglio l'Agente `CleaningStaff` che ogni configurabile ore passi e applichi `-90% viral_load` da tutti gli item statici intercettati.*

## Sprint 5: V1 Polish & Advanced Analytics (Settimane 6-8)

- **US-4.1**: *Come Analista o Medico Primario, cliccando su Paziente diventato positivo infetto durante la UI-Session, voglio aprire il Traceability Tree (catena sorgente: chi l'ha toccato per ultimo unito al fallimento d'igiene registrato dal sensore).*
- **US-4.2**: *Come Data Scientist, voglio un modulo CI CLI "Hessian-Run": dare in pasto 5 file JSON Scenario differenti, silenziare l'export video o animazioni, e computare 50.000 ore di incidenza generandomi solo tabelle Excel esportabili su rischio epidemiologico predittivo dei macro scenari.*
