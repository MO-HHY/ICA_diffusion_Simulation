# Validazione Scientifica, Integrità e Testing

Poiché questo sistema agirà come un Predictive Modeling Engine Hospital-Grade e non come un semplice 'Gametoy', occorrono test netti a validarne l'output matematico.

## 1. Replay Assoluto (Determinismo Stocastico)

Tutti i framework pseudocausali sono basati un Random Number Generator guidato.
Configurare due volte lo script Python usando `seed=1405` come attributo del JSON dovrà condurre matematicamente a vettori temporali e spostamenti millesimali sovrapponibili. Le due esecuzioni genereranno un EventLog con *Hash SHA-256 identico bit-per-bit*.
Questo approccio archivia, valida e stabilizza lo scenario di base pre-modifica codice.

## 2. Unit Test Code Specific (Contaminazione e Log-Reduction)

- `test_hand_washing_efficacy_stats()`:
  - **Setup**: Si instanziano in Headless 1000 eventi virtuali "HYGIENE_WASH" imponendo il prodotto disinfettante all'`85%` di validità ed il param `nurse_base_compliance=100%`.
  - **Assert**: Test verificherà che la somma prelavaggio / post lavaggio dell'agente generi la differenza stabilita `mean_load_after <= 0.15 * pre_load`, validando l'intercettazione dei drop rate.

## 3. Sanity Checks Epidemiologici

Scenario testing avanzato per testare le estremità dei protocolli previsti dalle curve SIR:

### Scenario A: Test Pathways Veloci (Influenza-like)

- Ereditare Patogeno = Modello Respiratorio (Surface decay accelerato < 4 ore).
- Eliminare i vettori diretti asintomatici "Non previsti", spegnendo mani interrotte post-visite per 12 turni.
- Se l'Epidemiologia risponde ad evidenza d'aria, l'assenza di drop sulle "Maniglie e Tavolini" (Fomiti) deve risultare nello scaricamento a terra del tasso derivato R0 in tempi ridotti, annullando a fine run la probabilità d'incidenza trasversale.

### Scenario B: Test Robustezza Resistiva (MRSA)

- Settare il patogeno su Altissima Emivita (Decadimento dopo giorni, = 72H+).
- Interrompere le attività della componente agent "Pulizie/Cleaners" annullando decurtazioni d'area.
- Settare una Compliance Staff Umani = al 100% solo ed sclusivamente prima di manipolare paziente e al 0% dopo paziente al tatto dell'elemento inanimato in uscita.
- **Risultato Obbligato Validato**: Il sistema deve causare Spike infettivi a ritardo temporale (Delay Effect), confermando il Teorema cardine per cui disinfettarsi escludendo la detergenza dell'arredo per il prossimo agente entrante non abbassa il fattore cross-fomite globale, perpetrando il focolaio nel reparto.
- *Conclusione Scientifica Visualizzabile*: Il primario o lo student visualizzando questo modulo capisce l'integrazione obbligatoria del pulire il corridoio/vassoi tanto quanto toccare il guanto paziente.
