# Parametri di Scenario e Dataset

Questo documento elenca i parametri configurabili per editare il comportamento dinamico della simulazione.

## Patogeni (Preset Default)

| Parametro | Tipo | Influenza-like | MRSA-like | Significato |
|-----------|------|----------------|-----------|-------------|
| `base_transmission_prob` | Float | `0.40` | `0.15` | Probabilità base stocastica di contagio per singolo contatto a rischio. |
| `surface_half_life_hrs` | Float | `4.0` | `72.0` | Tempo biologico di dimezzamento della carica vitale del patogeno sulle superfici. |
| `hands_half_life_mins` | Float | `15.0` | `60.0` | Tempo di dimezzamento della carica su mani (prima di morte naturale o lavaggio). |

## Parametri di Scenario Globale e Ospedaliero

I parametri che l'utente può variare per simulare scenari What-If, isolando i fattori di rischio:

| Categoria | Parametro | Range/Tipo | Default | Regola l'Impatto su: |
|-----------|-----------|------------|---------|-----------------------|
| Layout    | `total_beds` | `Int (10-100)` | `20` | Dimensione del reparto. |
| Layout    | `isolation_pct` | `Float (0-1)` | `0.1` | % di stanze configurate con protocolli di isolamento rigoroso. |
| Igiene    | `base_compliance` | `Float (0-1)` | `0.6` | Probabilità globale media di adesione all'igiene delle mani. |
| Igiene    | `isolation_modifier` | `Float (>1)` | `1.5` | Moltiplicatore compliance: l'operatore presta più attenzione se la stanza è isolata. |
| Igiene    | `gel_log_reduction` | `Float (0-1)` | `0.99` | Percentuale di carica patogena distrutta dall'uso corretto di Gel Idroalcolico. |
| Staffing  | `nurse_per_bed` | `Float (0-1)` | `0.2` | Carico di lavoro (Meno infermieri = turno più frenetico = crolla il tempo per igiene). |
| Cleaning  | `cleaning_frequency_hrs` | `Int (1-24)` | `8` | Intervallo ore tra due cicli ordinari di pulizie ambientali da parte delle OSS. |
| Cleaning  | `cleaning_efficacy` | `Float (0-1)` | `0.85` | Efficacia dei prodotti usati: log-reduction sulle superfici toccate dal team di pulizia. |
