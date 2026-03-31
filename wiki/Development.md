# Development

Guida per sviluppatori che vogliono contribuire all'integrazione Emmeti Mirai.

## 🚀 Come iniziare

### Prerequisiti

- Python 3.9+
- Home Assistant Development Environment
- Git
- Conoscenza base di Modbus e asyncio

### Setup ambiente di sviluppo

1. **Clona il repository**:
```bash
git clone https://github.com/stefanogelmini/HomeAssistant_EmmetiMirai.git
cd HomeAssistant_EmmetiMirai
```

2. **Installa dipendenze**:
```bash
pip install -e .
pip install -r requirements-dev.txt
```

3. **Configura pre-commit hooks**:
```bash
pre-commit install
```

## 📁 Struttura progetto

```
emmeti_mirai/
├── __init__.py              # Inizializzazione integrazione
├── manifest.json            # Metadati integrazione
├── config_flow.py           # Flusso configurazione
├── coordinator.py           # Coordinatore dati
├── modbus_client.py         # Client Modbus
├── const.py                 # Costanti e registri
├── entity_base.py           # Classe base entità
├── sensor.py                # Entità sensori
├── number.py                # Entità controlli numerici
├── switch.py                # Entità interruttori
├── select.py                # Entità selettori
├── binary_sensor.py         # Entità sensori binari
├── strings.json             # Stringhe UI
├── hacs.json               # Configurazione HACS
└── translations/            # Traduzioni
    ├── en.json
    └── it.json
```

## 🔧 Aggiungere nuove entità

### 1. Definisci i registri

Aggiungi i nuovi registri in `const.py`:

```python
# Registri sensori
REGISTERS = {
    # ... registri esistenti ...
    "nuovo_sensore": {
        "address": 40030,
        "count": 1,
        "scale": 0.1,
        "unit": "°C",
        "description": "Nuovo sensore temperatura"
    }
}
```

### 2. Crea l'entità

In `sensor.py`, aggiungi la nuova entità:

```python
class EmmetiMiraiNuovoSensoreSensor(EmmetiMiraiSensor):
    """Sensore nuovo."""

    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator, config_entry)
        self._register_key = "nuovo_sensore"

    @property
    def unique_id(self):
        return f"{self._config_entry.entry_id}_nuovo_sensore"

    @property
    def name(self):
        return "Nuovo Sensore"
```

### 3. Registra l'entità

In `__init__.py`, aggiungi al setup:

```python
async def async_setup_entry(hass, entry, async_add_entities):
    # ... setup esistente ...

    sensors = [
        # ... sensori esistenti ...
        EmmetiMiraiNuovoSensoreSensor(coordinator, entry),
    ]

    async_add_entities(sensors)
```

## 🧪 Testing

### Test unitari

```bash
# Esegui tutti i test
pytest

# Test specifici
pytest tests/test_modbus_client.py

# Con coverage
pytest --cov=emmeti_mirai --cov-report=html
```

### Test di integrazione

```bash
# Test con HA
hass -c config_test --script check_config

# Test manuale
python -m emmeti_mirai.test_integration
```

### Script di test Modbus

```bash
# Test connessione
python test_modbus.py --host 192.168.1.200 --verbose

# Test registro specifico
python test_modbus.py --host 192.168.1.200 --register 40001
```

## 📋 Linee guida codice

### Stile codice

- **Black**: Formattazione automatica
- **isort**: Ordinamento import
- **flake8**: Linting
- **mypy**: Type checking

```bash
# Formatta codice
black emmeti_mirai/
isort emmeti_mirai/

# Controlla qualità
flake8 emmeti_mirai/
mypy emmeti_mirai/
```

### Convenzioni

- **Nomi classi**: PascalCase
- **Nomi metodi/funzioni**: snake_case
- **Costanti**: UPPER_CASE
- **Docstrings**: Google style

### Esempio entità

```python
class EmmetiMiraiTemperatureSensor(EmmetiMiraiSensor):
    """Sensore temperatura ambiente interno.

    Legge la temperatura dall'indirizzo 40001 con scaling 0.1.
    """

    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator, config_entry)
        self._register_key = "temperatura_ambiente_interno"

    @property
    def unique_id(self):
        """ID univoco del sensore."""
        return f"{self._config_entry.entry_id}_temperatura_ambiente_interno"

    @property
    def name(self):
        """Nome visualizzato."""
        return "Temperatura Ambiente Interno"

    @property
    def device_class(self):
        """Classe dispositivo per UI."""
        return SensorDeviceClass.TEMPERATURE

    @property
    def state_class(self):
        """Classe stato per statistiche."""
        return SensorStateClass.MEASUREMENT

    @property
    def native_unit_of_measurement(self):
        """Unità di misura."""
        return UnitOfTemperature.CELSIUS

    @property
    def native_value(self):
        """Valore corrente."""
        return self.coordinator.get_register_value(self._register_key)
```

## 🔄 Versioning

Il progetto usa [Semantic Versioning](https://semver.org/):

- **MAJOR**: Cambiamenti breaking
- **MINOR**: Nuove funzionalità backward-compatible
- **PATCH**: Bug fixes

### Release process

1. **Aggiorna CHANGELOG.md**
2. **Aggiorna version in manifest.json**
3. **Crea tag**: `git tag v1.2.3`
4. **Push**: `git push origin main --tags`
5. **GitHub Release**: Crea release con changelog

## 🤝 Contributi

### Processo PR

1. **Fork** il repository
2. **Crea branch**: `git checkout -b feature/nome-feature`
3. **Commit**: `git commit -m "feat: aggiungi nuova feature"`
4. **Push**: `git push origin feature/nome-feature`
5. **PR**: Apri Pull Request

### Template commit

```
type(scope): description

[body]

[footer]
```

**Types**: feat, fix, docs, style, refactor, test, chore

## 📚 Risorse utili

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Modbus Protocol](https://modbus.org/)
- [PyModbus Documentation](https://pymodbus.readthedocs.io/)
- [HACS Integration Guide](https://hacs.xyz/docs/publish/start)

## 🐛 Debug

### Log livello debug

```python
import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("Debug message: %s", variable)
```

### Breakpoint interattivo

```python
import pdb; pdb.set_trace()
```

### Monitora Modbus

```bash
# Cattura traffico Modbus
tcpdump -i eth0 port 502 -w modbus_traffic.pcap
```

---

[[Troubleshooting|← Risoluzione problemi]] | [[Home|Torna alla home]]