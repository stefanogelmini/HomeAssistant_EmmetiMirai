# Configuration

Guida dettagliata alla configurazione dell'integrazione Emmeti Mirai.

## 🔧 Parametri di configurazione

### Parametri obbligatori

| Parametro | Descrizione | Default | Esempio |
|-----------|-------------|---------|---------|
| **Host** | Indirizzo IP della pompa di calore | - | 192.168.1.200 |
| **Porta** | Porta Modbus TCP | 502 | 502 |
| **ID Slave** | ID del dispositivo Modbus | 1 | 1 |

### Parametri opzionali

| Parametro | Descrizione | Default |
|-----------|-------------|---------|
| **Nome** | Nome personalizzato dell'integrazione | Emmeti Mirai |
| **Timeout** | Timeout connessione (secondi) | 5 |

## 📊 Entità create automaticamente

Dopo la configurazione, l'integrazione crea le seguenti entità:

### Sensori (sensor.*)
- **Temperatura ambiente interno**: `sensor.emmeti_mirai_temperatura_ambiente_interno`
- **Temperatura esterna**: `sensor.emmeti_mirai_temperatura_esterna`
- **Temperatura ACS**: `sensor.emmeti_mirai_temperatura_acs`
- **Consumo energetico**: `sensor.emmeti_mirai_consumo_energetico`
- **Stato operativo**: `sensor.emmeti_mirai_stato_operativo`
- **Ore compressore**: `sensor.emmeti_mirai_ore_compressore`
- **COP (Coefficiente di Performance)**: `sensor.emmeti_mirai_cop`

### Controlli (number.*)
- **Setpoint temperatura**: `number.emmeti_mirai_setpoint_temperatura`
- **Setpoint ACS**: `number.emmeti_mirai_setpoint_acs`

### Interruttori (switch.*)
- **Resistenza ACS**: `switch.emmeti_mirai_resistenza_acs`
- **Pompa ricircolo ACS**: `switch.emmeti_mirai_pompa_ricircolo_acs`
- **Centralina solare**: `switch.emmeti_mirai_centralina_solare`

### Selettori (select.*)
- **Modalità operativa**: `select.emmeti_mirai_modalita_operativa`

## 🎛️ Configurazione avanzata

### Modifica configurazione esistente

1. Vai su **Impostazioni** → **Dispositivi e servizi**
2. Trova "Emmeti Mirai" nell'elenco
3. Clicca su **Configura**
4. Modifica i parametri desiderati

### Rimozione integrazione

1. Vai su **Impostazioni** → **Dispositivi e servizi**
2. Trova "Emmeti Mirai"
3. Clicca sui **...** → **Elimina**
4. Conferma l'eliminazione

## 🔄 Aggiornamento configurazione

L'integrazione supporta la riconfigurazione senza riavvio completo:

1. Modifica i parametri tramite l'interfaccia
2. L'integrazione si riconnette automaticamente
3. Le entità esistenti vengono aggiornate

## 📈 Monitoraggio connessione

### Stato connessione
- **Entità**: `binary_sensor.emmeti_mirai_connessione`
- **Stati**: `on` (connesso), `off` (disconnesso)

### Log di connessione
I log di connessione sono disponibili in:
- **Impostazioni** → **Sistema** → **Log**
- Filtra per "emmeti_mirai"

### Debug avanzato
Per debug dettagliato, aggiungi al `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.emmeti_mirai: debug
```

## ⚠️ Considerazioni di sicurezza

- L'integrazione comunica tramite Modbus TCP non crittografato
- Assicurati che la rete locale sia sicura
- Considera l'uso di VLAN dedicate per dispositivi IoT
- Mantieni firmware della pompa aggiornato

## 🔧 Troubleshooting configurazione

### Problema: "Impossibile connettere al dispositivo"
**Soluzioni:**
- Verifica indirizzo IP corretto
- Controlla che la porta 502 sia aperta
- Verifica ID slave corretto
- Controlla firewall/router

### Problema: "Timeout connessione"
**Soluzioni:**
- Aumenta il timeout nelle impostazioni
- Verifica latenza di rete
- Controlla carico del dispositivo

### Problema: "Valori non aggiornati"
**Soluzioni:**
- Verifica connessione stabile
- Controlla log per errori
- Riavvia l'integrazione

---

[[Installation|← Installazione]] | [[Entities|Entità →]]