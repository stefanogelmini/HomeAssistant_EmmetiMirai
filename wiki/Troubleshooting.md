# Troubleshooting

Guida alla risoluzione dei problemi più comuni con l'integrazione Emmeti Mirai.

## 🔍 Diagnostica iniziale

### 1. Verifica connessione di base

Prima di tutto, verifica che la pompa sia raggiungibile:

```bash
# Test connessione TCP
telnet 192.168.1.200 502

# Oppure con PowerShell
Test-NetConnection -ComputerName 192.168.1.200 -Port 502
```

### 2. Controlla i log di Home Assistant

Vai su **Impostazioni** → **Sistema** → **Log** e cerca errori relativi a "emmeti_mirai".

### 3. Test con script standalone

Usa lo script di test incluso per verificare la comunicazione Modbus:

```bash
cd /config
python custom_components/emmeti_mirai/test_modbus.py --host 192.168.1.200
```

## 🚨 Problemi comuni e soluzioni

### "Impossibile connettere al dispositivo"

**Sintomi:**
- Entità mostrano "non disponibile"
- Log mostrano "Connection timeout"

**Soluzioni:**
1. **Verifica indirizzo IP**: Assicurati che l'IP configurato sia corretto
2. **Controlla porta**: La porta 502 deve essere aperta sul dispositivo
3. **Firewall/Router**: Verifica che non ci siano regole di blocco
4. **Rete**: Assicurati che HA e la pompa siano sulla stessa subnet
5. **ID Slave**: Verifica che l'ID slave (default: 1) sia corretto

### "Timeout connessione"

**Sintomi:**
- Connessione intermittente
- Valori che si aggiornano sporadicamente

**Soluzioni:**
1. **Aumenta timeout**: Nella configurazione, imposta timeout a 10-15 secondi
2. **Riduci polling**: Aumenta intervallo di polling a 30-60 secondi
3. **Rete lenta**: Verifica latenza di rete tra HA e pompa

### "Valori non realistici"

**Sintomi:**
- Temperature a 0°C o 999°C
- COP negativo o troppo alto

**Soluzioni:**
1. **Byte order**: Verifica che i registri usino il byte order corretto
2. **Scaling**: Controlla i fattori di scala per i valori
3. **Firmware**: Aggiorna firmware della pompa se possibile

### "Entità non disponibili dopo riavvio"

**Sintomi:**
- Dopo riavvio HA, alcune entità rimangono "non disponibili"

**Soluzioni:**
1. **Ordine avvio**: Assicurati che l'integrazione si avvii dopo la rete
2. **Dipendenze**: Verifica che pymodbus sia installato correttamente
3. **Configurazione**: Ricarica configurazione manuale

## 🔧 Debug avanzato

### Abilita logging dettagliato

Aggiungi al tuo `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.emmeti_mirai: debug
    pymodbus: debug
```

### Test registri specifici

Usa lo script di test per verificare registri individuali:

```python
# In test_modbus.py
client.read_holding_registers(address=40001, count=1, device_id=1)  # Temperatura
```

### Monitora traffico di rete

```bash
# Su Linux/macOS
tcpdump -i eth0 host 192.168.1.200 and port 502

# Su Windows (con Wireshark)
# Cattura traffico su porta 502
```

## 📊 Analisi prestazioni

### Monitora utilizzo risorse

- **CPU**: L'integrazione dovrebbe usare <1% CPU
- **Memoria**: ~10-20MB per istanza
- **Rete**: ~1-2KB per polling (ogni 30s)

### Ottimizzazioni

1. **Intervallo polling**: Aumenta a 60s se la pompa è lenta
2. **Timeout**: Riduci a 3s su reti veloci
3. **Registri batch**: Leggi più registri insieme quando possibile

## 🔄 Ripristino e recovery

### Ricarica integrazione

```yaml
# In configuration.yaml
# Aggiungi temporaneamente per debug
emmeti_mirai:
  - host: 192.168.1.200
    reload: true
```

### Reset configurazione

1. Rimuovi l'integrazione
2. Riavvia HA
3. Reinstalla e riconfigura

### Pulizia cache

```bash
# Elimina eventuali file cache
rm -rf /config/.storage/emmeti_mirai*
```

## 🆘 Contatto supporto

Se i problemi persistono:

1. **Raccogli informazioni**:
   - Versione HA e integrazione
   - Log completi (con debug abilitato)
   - Output dello script di test
   - Configurazione rete

2. **Apri issue**: [GitHub Issues](https://github.com/stefanogelmini/HomeAssistant_EmmetiMirai/issues)

3. **Forum community**: [Home Assistant Community](https://community.home-assistant.io)

## 📋 Checklist troubleshooting

- [ ] IP e porta corretti
- [ ] ID slave corretto
- [ ] Connettività di rete
- [ ] Firewall/router configurati
- [ ] Firmware pompa aggiornato
- [ ] Versione HA compatibile
- [ ] pymodbus installato
- [ ] Log controllati
- [ ] Script di test eseguito

---

[[Entities|← Entità]] | [[Development|Sviluppo →]]