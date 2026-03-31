# Wiki Documentation

Questa cartella contiene la documentazione completa per la wiki di GitHub dell'integrazione Emmeti Mirai.

## 📄 File inclusi

- **Home.md** - Pagina principale della wiki
- **Installation.md** - Guida all'installazione
- **Configuration.md** - Configurazione dettagliata
- **Entities.md** - Elenco completo delle entità
- **Troubleshooting.md** - Guida alla risoluzione problemi
- **Development.md** - Guida per sviluppatori

## 🚀 Come pubblicare su GitHub Wiki

### Metodo 1: Copia manuale

1. Vai su https://github.com/stefanogelmini/HomeAssistant_EmmetiMirai/wiki
2. Crea una nuova pagina per ogni file `.md`
3. Copia il contenuto di ogni file
4. Salva la pagina

### Metodo 2: Script automatico

```bash
# Script per pubblicare automaticamente (richiede GitHub CLI)
for file in wiki/*.md; do
    title=$(basename "$file" .md)
    gh wiki pages create "$title" --content "$file"
done
```

### Metodo 3: Git clone wiki

```bash
# Clona la wiki come repository separato
git clone https://github.com/stefanogelmini/HomeAssistant_EmmetiMirai.wiki.git
cd HomeAssistant_EmmetiMirai.wiki

# Copia i file
cp ../HomeAssistant_EmmetiMirai/wiki/*.md .

# Commit e push
git add .
git commit -m "Update documentation"
git push
```

## 📝 Manutenzione

- Aggiorna questi file quando fai modifiche al codice
- Mantieni sincronizzato con il CHANGELOG.md
- Usa collegamenti interni alla wiki: `[[Page|Link Text]]`

## 🎯 Struttura consigliata wiki

```
Home
├── Installation
├── Configuration
├── Entities
│   ├── Sensors
│   ├── Controls
│   └── Automations
├── Troubleshooting
└── Development
    ├── Setup
    ├── Testing
    └── Contributing
```

## 🔗 Link utili

- [GitHub Wiki Guide](https://docs.github.com/en/communities/documenting-your-project-with-wikis)
- [Markdown Guide](https://www.markdownguide.org/)
- [Home Assistant Documentation Style](https://developers.home-assistant.io/docs/documenting/)