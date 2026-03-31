# Entities

Elenco completo delle entità create dall'integrazione Emmeti Mirai.

## 📊 Sensori (Sensors)

### Temperature
| Entità | Descrizione | Unità | Registro |
|--------|-------------|-------|----------|
| `sensor.emmeti_mirai_temperatura_ambiente_interno` | Temperatura ambiente interno rilevata | °C | 40001 |
| `sensor.emmeti_mirai_temperatura_esterna` | Temperatura esterna | °C | 40002 |
| `sensor.emmeti_mirai_temperatura_acs` | Temperatura acqua calda sanitaria | °C | 40003 |
| `sensor.emmeti_mirai_temperatura_mandata` | Temperatura acqua in uscita | °C | 40004 |
| `sensor.emmeti_mirai_temperatura_ritorno` | Temperatura acqua in ritorno | °C | 40005 |

### Energetici
| Entità | Descrizione | Unità | Registro |
|--------|-------------|-------|----------|
| `sensor.emmeti_mirai_consumo_energetico` | Potenza assorbita attuale | W | 40010 |
| `sensor.emmeti_mirai_cop` | Coefficiente di Performance | - | 40011 |
| `sensor.emmeti_mirai_ore_compressore` | Ore totali funzionamento compressore | h | 40012 |

### Stati operativi
| Entità | Descrizione | Valori | Registro |
|--------|-------------|--------|----------|
| `sensor.emmeti_mirai_stato_operativo` | Stato corrente del sistema | Idle/Heating/Cooling/DHW | 40020 |
| `sensor.emmeti_mirai_modalita_attiva` | Modalità operativa attiva | Heating/Cooling/DHW/Off | 40021 |
| `sensor.emmeti_mirai_allarmi` | Codici allarme attivi | Lista codici | 40022 |

## 🎛️ Controlli (Controls)

### Temperature setpoint
| Entità | Descrizione | Range | Unità | Registro |
|--------|-------------|-------|-------|----------|
| `number.emmeti_mirai_setpoint_riscaldamento` | Setpoint temperatura riscaldamento | 15-30 | °C | 41001 |
| `number.emmeti_mirai_setpoint_raffreddamento` | Setpoint temperatura raffreddamento | 18-25 | °C | 41002 |
| `number.emmeti_mirai_setpoint_acs_giorno` | Setpoint ACS giorno | 40-65 | °C | 41003 |
| `number.emmeti_mirai_setpoint_acs_notte` | Setpoint ACS notte | 35-60 | °C | 41004 |

### Temporizzazioni
| Entità | Descrizione | Range | Unità | Registro |
|--------|-------------|-------|-------|----------|
| `number.emmeti_mirai_tempo_ricircolo_acs` | Tempo ricircolo ACS | 0-60 | min | 41010 |

## 🔄 Interruttori (Switches)

| Entità | Descrizione | Registro |
|--------|-------------|----------|
| `switch.emmeti_mirai_resistenza_acs` | Abilita/disabilita resistenza ACS | 42001 |
| `switch.emmeti_mirai_pompa_ricircolo_acs` | Controllo pompa ricircolo ACS | 42002 |
| `switch.emmeti_mirai_centralina_solare` | Abilita/disabilita integrazione solare | 42003 |
| `switch.emmeti_mirai_modalita_silenziosa` | Attiva modalità silenziosa | 42004 |

## 📋 Selettori (Selects)

### Modalità operative
| Entità | Descrizione | Opzioni | Registro |
|--------|-------------|---------|----------|
| `select.emmeti_mirai_modalita_operativa` | Modalità principale | Auto/Heating/Cooling/DHW/Off | 43001 |
| `select.emmeti_mirai_programma_settimanale` | Programma settimanale | Program1/Program2/Program3/Off | 43002 |

## 🔍 Sensori binari (Binary Sensors)

| Entità | Descrizione | Registro |
|--------|-------------|----------|
| `binary_sensor.emmeti_mirai_compressione_attiva` | Stato compressore | 44001 |
| `binary_sensor.emmeti_mirai_riscaldamento_attivo` | Riscaldamento attivo | 44002 |
| `binary_sensor.emmeti_mirai_raffreddamento_attivo` | Raffreddamento attivo | 44003 |
| `binary_sensor.emmeti_mirai_acs_attivo` | Produzione ACS attiva | 44004 |
| `binary_sensor.emmeti_mirai_allarme_attivo` | Presenza allarmi | 44005 |
| `binary_sensor.emmeti_mirai_connessione` | Stato connessione Modbus | - |

## 📈 Utilizzo in automazioni

### Esempi di automazione

#### 1. Notifica quando temperatura troppo bassa
```yaml
automation:
  - alias: "Notifica temperatura bassa"
    trigger:
      platform: numeric_state
      entity_id: sensor.emmeti_mirai_temperatura_ambiente_interno
      below: 18
    action:
      service: notify.mobile_app
      data:
        message: "Temperatura ambiente troppo bassa!"
```

#### 2. Attiva resistenza ACS quando necessario
```yaml
automation:
  - alias: "Attiva resistenza ACS"
    trigger:
      platform: numeric_state
      entity_id: sensor.emmeti_mirai_temperatura_acs
      below: 45
    action:
      service: switch.turn_on
      target:
        entity_id: switch.emmeti_mirai_resistenza_acs
```

#### 3. Cambio modalità stagionale
```yaml
automation:
  - alias: "Modalità estiva"
    trigger:
      platform: numeric_state
      entity_id: sensor.emmeti_mirai_temperatura_esterna
      above: 20
    action:
      service: select.select_option
      target:
        entity_id: select.emmeti_mirai_modalita_operativa
      data:
        option: "Cooling"
```

## 🔧 Attributi aggiuntivi

Molte entità includono attributi aggiuntivi:

- **Ultimo aggiornamento**: Timestamp dell'ultimo valore valido
- **Qualità segnale**: Indicatore affidabilità lettura
- **Unità di misura**: Conferma unità utilizzata
- **Range valido**: Min/max valori accettabili

## 📊 Dashboard Lovelace

### Esempio card temperatura
```yaml
type: entities
entities:
  - sensor.emmeti_mirai_temperatura_ambiente_interno
  - sensor.emmeti_mirai_temperatura_esterna
  - number.emmeti_mirai_setpoint_riscaldamento
title: Controllo Temperatura
```

### Esempio card energetica
```yaml
type: gauge
entity: sensor.emmeti_mirai_cop
min: 0
max: 5
title: COP Pompa di Calore
```

---

[[Configuration|← Configurazione]] | [[Troubleshooting|Risoluzione problemi →]]