# Installation

Questa guida spiega come installare l'integrazione Emmeti Mirai per Home Assistant.

## 📋 Prerequisiti

- Home Assistant (versione 2023.6.0 o superiore)
- Pompa di calore Emmeti Mirai connessa alla rete
- Indirizzo IP della pompa di calore
- Porta Modbus (default: 502)
- ID slave Modbus (default: 1)

## 🔧 Metodi di installazione

### Opzione 1: HACS (Raccomandato)

1. Assicurati di avere [HACS](https://hacs.xyz/) installato
2. In Home Assistant, vai su **HACS** → **Integrazioni**
3. Clicca su **Esplora e scarica repository**
4. Cerca "Emmeti Mirai"
5. Seleziona il repository e clicca **Scarica**
6. Riavvia Home Assistant

### Opzione 2: Installazione manuale

1. Scarica l'ultima release dal [repository GitHub](https://github.com/stefanogelmini/HomeAssistant_EmmetiMirai/releases)
2. Estrai il contenuto nella cartella `custom_components/emmeti_mirai/`
3. Riavvia Home Assistant

```bash
# Esempio struttura finale
config/
├── custom_components/
│   └── emmeti_mirai/
│       ├── __init__.py
│       ├── manifest.json
│       └── ...
```

## ⚙️ Configurazione iniziale

Dopo l'installazione:

1. Vai su **Impostazioni** → **Dispositivi e servizi**
2. Clicca su **Aggiungi integrazione**
3. Cerca "Emmeti Mirai"
4. Inserisci i parametri richiesti:
   - **Host**: Indirizzo IP della pompa (es. 192.168.1.200)
   - **Porta**: Porta Modbus (default: 502)
   - **ID Slave**: ID del dispositivo Modbus (default: 1)
   - **Nome**: Nome personalizzato per l'integrazione

## ✅ Verifica installazione

Dopo la configurazione, dovresti vedere:

- Un nuovo dispositivo "Emmeti Mirai" nei dispositivi
- Multiple entità per sensori e controlli
- Log di connessione riuscita in Home Assistant

## 🔄 Aggiornamenti

### Via HACS
- HACS notificherà automaticamente gli aggiornamenti
- Vai su **HACS** → **Integrazioni** → **Emmeti Mirai** → **Aggiorna**

### Manuale
- Scarica la nuova versione
- Sostituisci i file in `custom_components/emmeti_mirai/`
- Riavvia Home Assistant

## 🐛 Problemi comuni

Se l'installazione fallisce:

1. **Controlla i log**: Vai su **Impostazioni** → **Sistema** → **Log**
2. **Verifica connettività**: Assicurati che la pompa sia raggiungibile
3. **Controlla versione HA**: Assicurati di avere HA 2023.6.0+

Per problemi specifici, consulta la pagina [[Troubleshooting|Risoluzione problemi]].

---

[[Home|← Torna alla home]] | [[Configuration|Configurazione →]]