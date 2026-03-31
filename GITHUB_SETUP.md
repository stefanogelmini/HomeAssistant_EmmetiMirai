# Pubblicare su GitHub

Questo repository è stato inizializzato localmente. Segui i passi sotto per pubblicarlo su GitHub.

## Step 1: Crea un nuovo repository su GitHub

1. Vai su [hhttps://github.com/stefanogelmini/](https://github.com/stefanogelmini)
2. **Repository name**: `Emmeti_Mirai`
3. **Description**: "Emmeti Mirai Home Assistant Integration - Modbus TCP support"
4. **Visibility**: Seleziona "Public" (o "Private" per sviluppo privato)
5. **Inizialize**: NON selezionare nessuna opzione (il repo esiste già localmente)
6. Clicca **"Create repository"**

## Step 2: Aggiungi il remote e pusha

```bash
cd "H:\Emmeti_Mirai"

# Aggiungi il remote origin (sostituisci USERNAME con il tuo username GitHub)
git remote add origin https://github.com/stefanogelmini/HomeAssistant_EmmetiMirai.git

# Rinomina il branch principale se necessario (Github usa 'main' di default)
git branch -M master main

# Pusha il branch e i tag
git push -u origin main
git push origin v1.0.0
```

## Step 3: Verifica il repository

- Vai su: `https://github.com/USERNAME/Emmeti_Mirai`
- Verifica che tutti i file siano presenti
- Clicca su "Releases" e verifica che `v1.0.0` appaia

## Step 4 (Opzionale): Aggiungi Topics

Nel repository GitHub, aggiungi questi topics (About → Add topics):
- `home-assistant`
- `integration`
- `emmeti`
- `heat-pump`
- `modbus`

## Step 5 (Opzionale): Abilita GitHub Actions

Nel repository:
1. Vai a **Settings → Actions → General**
2. Assicurati che "Allow all actions and reusable workflows" sia selezionato
3. I workflow CI/CD in `.github/workflows/` verranno eseguiti automaticamente

## Gestione dei Tag e Releases

### Per creare una nuova versione:

```bash
# 1. Crea un branch per la feature
git checkout -b feature/my-feature

# 2. Fai i tuoi cambiamenti

# 3. Aggiorna il versionamento
git checkout main
# Aggiorna: manifest.json, setup.py, CHANGELOG.md

# 4. Commit
git add .
git commit -m "Bump version to v1.1.0"

# 5. Tag
git tag -a v1.1.0 -m "Release version 1.1.0

- Descrizione dei cambiamenti
- Migliorie"

# 6. Pusha
git push origin main
git push origin v1.1.0
```

### Creare una Release su GitHub

1. Vai al repository GitHub
2. Clicca su **"Releases"**
3. Clicca su **"Create a new release"**
4. Seleziona il tag (es. `v1.1.0`)
5. Titolo: `v1.1.0 - Nome Release`
6. Descrizione: Copia dal CHANGELOG.md
7. Clicca **"Create Release"**

## Linee guida per il Versioning

Usa [Semantic Versioning](https://semver.org/):

- **v1.0.0** → v1.0.1 (patch - bug fixes)
- **v1.0.0** → v1.1.0 (minor - new features)
- **v1.0.0** → v2.0.0 (major - breaking changes)

## File di Configurazione

Il repository include:

- **`.gitignore`**: Escude file non necessari (\_\_pycache\_\_, *.pyc, etc.)
- **`setup.py`**: Per package distribution (PyPI in futuro)
- **`pyproject.toml`**: Configurazione moderna Python
- **`.github/workflows/python-lint.yml`**: CI/CD automatico
- **`README_DEVELOPMENT.md`**: Guida completa per sviluppatori
- **`CHANGELOG.md`**: Storico delle versioni
- **`LICENSE`**: MIT License

## Aggiornamenti Futuri

Quando aggiorni il componente in `z:\custom_components\emmeti_mirai\`:

```bash
# Opzione 1: Aggiorna dal source
robocopy "z:\custom_components\emmeti_mirai" "H:\Emmeti_Mirai\emmeti_mirai" /E

# Opzione 2: Fai il pull dal repository GitHub per mantenere in sync
cd "z:\custom_components\emmeti_mirai"
git pull https://github.com/stefanogelmini/HomeAssistant_EmmetiMirai.git main
```

---

**Done!** Il tuo repository è pronto su GitHub. 🚀
