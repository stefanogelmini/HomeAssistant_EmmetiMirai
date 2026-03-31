# Emmeti Mirai Development Guide

Questo documento descrive come contribuire e sviluppare l'integrazione Emmeti Mirai.

## Versioning

Questo progetto segue [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features backwards compatible
- **PATCH**: Bug fixes

Formato: `vMAJOR.MINOR.PATCH`

Esempi: `v1.0.0`, `v1.1.0`, `v1.0.1`

## Git Tags

### Creazione di un nuovo tag

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Listing tags

```bash
git tag -l
git log --oneline --all --decorate
```

### Bump versione

1. Aggiorna `manifest.json` → `version`
2. Aggiorna `setup.py` → `version`
3. Aggiorna `CHANGELOG.md`
4. Commit: `git commit -m "Bump version to v1.x.x"`
5. Tag: `git tag -a vX.X.X -m "Release version X.X.X"`
6. Push: `git push origin master --set-upstream && git push origin vX.X.X`

## Struttura del progetto

```
H:\Emmeti_Mirai/
├── __init__.py                      # Integrazione HA
├── manifest.json                    # Versione HA
├── const.py                         # Registri Modbus
├── config_flow.py                   # UI configurazione
├── coordinator.py                   # Coordinator HA
├── modbus_client.py                 # Client Modbus RTU/TCP
├── sensor.py
├── binary_sensor.py
├── number.py
├── select.py
├── switch.py
├── entity_base.py
├── test_integration.py
├── icons/
│   └── emmeti_mirai/
│       └── heat_pump.svg            # Icona personalizzata
├── translations/
│   ├── en.json
│   └── it.json
├── strings.json
├── README.md
├── hacs.json
├── .github/
│   └── workflows/
│       └── python-lint.yml          # CI/CD
├── LICENSE                          # MIT
├── CHANGELOG.md                     # Cambiamenti versione
├── README_DEVELOPMENT.md            # Questo file
├── setup.py                         # Setup package
├── pyproject.toml                   # Configurazione progetto
└── .gitignore                       # Git ignore
```

## Releases

### Processo di release

1. **Feature branch**: `git checkout -b feature/my-feature`
2. **Commit**: Fai i tuoi cambiamenti
3. **Update docs**: Aggiorna README, CHANGELOG
4. **Bump versione**: vedi sezione "Bump versione"
5. **Pull Request**: (se necessario)
6. **Tag**: Crea il tag per la release
7. **GitHub Release**: Crea una release su GitHub con le note dal CHANGELOG

### Elenco Release/Tag

```bash
git tag -l -n1          # Lista tag con annotazioni
git log --oneline -n 10 # Lista ultimi 10 commit
```

## Testing

```bash
python -m pytest test_integration.py -v
```

## Code Style

- **Black**: Formattazione codice
- **isort**: Ordinamento import
- **flake8**: Linting

```bash
black .
isort .
flake8 .
```

## CI/CD

GitHub Actions esegue automaticamente:
- `python-lint.yml`: Flake8, Black, isort checks

## Supporto Versioni

- Python: 3.11+
- Home Assistant: 2024.1+
- pymodbus: 3.0+

## Build Package

```bash
python -m pip install build
python -m build
```

Output in `dist/`

## Publish a PyPI (opzionale in futuro)

```bash
python -m twine upload dist/*
```
