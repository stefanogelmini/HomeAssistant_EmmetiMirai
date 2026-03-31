# Emmeti Mirai – Home Assistant Integration

Custom integration per interfacciare la pompa di calore **Emmeti Mirai** tramite **Modbus TCP** con Home Assistant.

---

## Caratteristiche

| Funzione | Dettaglio |
|----------|-----------|
| Protocollo | Modbus TCP |
| Configurazione | UI (Config Flow) – nessun file YAML da modificare |
| Polling | Configurabile (default 30 s) |
| Registri inclusi | Definiti in `const.py` (no `modbus.yaml` esterno) |
| Piattaforme HA | `sensor`, `binary_sensor`, `number`, `select`, `switch` |
| Opzioni | Aggiornabili a runtime senza riavvio |

---

## Installazione

### Manuale

1. Copia la cartella `emmeti_mirai/` in `<config>/custom_components/`
2. Riavvia Home Assistant
3. Vai in **Impostazioni → Dispositivi e servizi → Aggiungi integrazione**
4. Cerca **"Emmeti Mirai"**

### HACS (opzionale, se pubblicata)

Aggiungi come repository personalizzato in HACS e installa normalmente.

---

## Configurazione

Al primo avvio comparirà il form:

| Campo | Descrizione | Default |
|-------|-------------|---------|
| **Host / IP** | Indirizzo IP o hostname del gateway Modbus TCP | – |
| **Porta TCP** | Porta Modbus TCP | `502` |
| **Slave ID** | Indirizzo unità Modbus (1–247) | `1` |
| **Intervallo polling** | Frequenza di lettura in secondi (5–3600) | `30` |

L'integrazione testa la connessione prima di salvare. In caso di errore viene mostrato un messaggio specifico.

---

## Entità create

### Sensori (`sensor`)

| Entità | Registro | Unità | Descrizione |
|--------|----------|-------|-------------|
| `t_outdoor` | Input 0 | °C | Temperatura esterna |
| `t_water_in` | Input 1 | °C | Temperatura acqua ingresso |
| `t_water_out` | Input 2 | °C | Temperatura acqua uscita |
| `t_dhw` | Input 3 | °C | Temperatura ACS |
| `t_refrigerant_liquid` | Input 4 | °C | Temperatura refrigerante liquido |
| `t_refrigerant_suction` | Input 5 | °C | Temperatura refrigerante aspirazione |
| `t_compressor_discharge` | Input 6 | °C | Temperatura scarico compressore |
| `p_high` | Input 10 | bar | Pressione alta |
| `p_low` | Input 11 | bar | Pressione bassa |
| `power_input` | Input 20 | kW | Potenza assorbita |
| `power_output` | Input 21 | kW | Potenza termica prodotta |
| `cop` | Input 22 | – | COP istantaneo |
| `energy_total_kwh` | Input 23 | kWh | Energia totale consumata |
| `compressor_freq` | Input 30 | Hz | Frequenza compressore |
| `compressor_current` | Input 31 | A | Corrente compressore |
| `fan_speed` | Input 40 | rpm | Velocità ventilatore |
| `alarm_code` | Input 50 | – | Codice allarme attivo |

### Sensori binari (`binary_sensor`)

| Entità | Registro | Descrizione |
|--------|----------|-------------|
| `defrost_active` | Input 51 | Sbrinamento in corso |
| `pump_active` | Input 52 | Pompa acqua in funzione |

### Numeri / Setpoint (`number`)

| Entità | Registro | Range | Step | Descrizione |
|--------|----------|-------|------|-------------|
| `setpoint_heating` | Holding 100 | 20–60 °C | 0.5 | Setpoint riscaldamento |
| `setpoint_cooling` | Holding 101 | 7–25 °C | 0.5 | Setpoint raffreddamento |
| `setpoint_dhw` | Holding 102 | 40–60 °C | 1.0 | Setpoint ACS |

### Selezione modalità (`select`)

| Entità | Registro | Opzioni |
|--------|----------|---------|
| `operating_mode` | Holding 110 | Spento / Riscaldamento / Raffreddamento / ACS / Riscaldamento+ACS / Raffreddamento+ACS / Automatico |

### Interruttore (`switch`)

| Entità | Registro | Descrizione |
|--------|----------|-------------|
| `unit_on_off` | Holding 111 | Accensione / spegnimento unità |

---

## Personalizzare i registri

Tutti i registri sono definiti nella lista `MODBUS_REGISTERS` in `const.py`.  
Ogni entry supporta i seguenti campi:

```python
{
    "key": "nome_univoco",          # ID interno
    "name": "Nome HA",              # Nome visualizzato
    "register": 42,                 # Indirizzo Modbus
    "register_type": "input",       # holding | input | coil | discrete_input
    "data_type": "int16",           # int16 | uint16 | int32 | uint32 | float32 | bool
    "scale": 0.1,                   # Fattore di scala
    "offset": 0,                    # Offset post-scala
    "unit": "°C",                   # Unità HA (None se assente)
    "device_class": "temperature",  # Device class HA (None se assente)
    "state_class": "measurement",   # State class HA (None se assente)
    "entity_type": "sensor",        # sensor | binary_sensor | number | select | switch
    "writable": False,              # True per holding register scrivibili
    # Campi extra per number:
    "min_value": 20.0,
    "max_value": 60.0,
    "step": 0.5,
    # Campi extra per select:
    "options": {0: "Off", 1: "On"},
}
```

Dopo ogni modifica riavvia Home Assistant.

---

## Struttura file

```
custom_components/emmeti_mirai/
├── __init__.py          # Setup / teardown entry
├── config_flow.py       # UI Config Flow + Options Flow
├── const.py             # Costanti + MODBUS_REGISTERS (mappa completa)
├── coordinator.py       # DataUpdateCoordinator (polling)
├── entity_base.py       # Classe base condivisa
├── modbus_client.py     # Client Modbus TCP (pymodbus)
├── sensor.py            # Piattaforma sensor
├── binary_sensor.py     # Piattaforma binary_sensor
├── number.py            # Piattaforma number
├── select.py            # Piattaforma select
├── switch.py            # Piattaforma switch
├── manifest.json        # Metadati integrazione
├── strings.json         # Stringhe UI (en)
└── translations/
    ├── en.json
    └── it.json
```

---

## Dipendenze

- `pymodbus >= 3.6.9` (installata automaticamente da HA)

---

## Licenza

MIT
