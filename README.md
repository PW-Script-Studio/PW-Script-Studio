# 🎬 PW-Script-Studio

Ein Django-basiertes Script-Management-System mit getrennten Workflows für OFFENE und AKTIVE Aufträge.

## 🚀 Hauptfeatures

### Kritische Workflow-Trennung
- **OFFENE Aufträge (Bewerbungen)**: Titel wird GENERIERT, KEINE Serper API
- **AKTIVE Aufträge (Kundenprojekte)**: Titel vom KUNDEN vorgegeben, MIT Serper API

### 3-Kachel-System
1. **📋 Kachel 1: Auftragsverwaltung** - Verwaltung aller Aufträge mit Status-Tracking
2. **🔍 Kachel 2: Analyse** - Getrennte Workflows für verschiedene Auftragstypen
3. **📤 Kachel 3: Export** - Export in verschiedene Formate (PDF, DOCX, HTML)

## 🏗️ Projektstruktur

```
PW-Script-Studio/
├── apps/                           # Django Apps
│   ├── dashboard/                  # Hauptdashboard
│   ├── kachel1_auftragsverwaltung/ # Auftragsverwaltung
│   ├── kachel2_analyse/            # Analyse mit getrennten Workflows
│   │   ├── workflows_offen/        # OFFENE Aufträge (Bewerbungen)
│   │   ├── workflows_aktiv/        # AKTIVE Aufträge (Kundenprojekte)
│   │   └── services/               # API Services
│   ├── kachel3_export/             # Export-Funktionen
│   └── api/                        # REST API
├── config/                         # Django Konfiguration
├── core/                           # Gemeinsame Funktionalitäten
├── requirements.txt                # Python Dependencies
└── .env.template                   # Environment Template
```

## 🔧 Installation

### 1. Repository klonen
```bash
git clone https://github.com/[USERNAME]/PW-Script-Studio.git
cd PW-Script-Studio
```

### 2. Virtual Environment erstellen
```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
# oder
source .venv/bin/activate      # Linux/Mac
```

### 3. Dependencies installieren
```bash
pip install -r requirements.txt
```

### 4. Environment konfigurieren
```bash
cp .env.template .env
# .env Datei mit eigenen API-Keys bearbeiten
```

### 5. Datenbank migrieren
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Superuser erstellen
```bash
python manage.py createsuperuser
```

### 7. Server starten
```bash
python manage.py runserver
```

## 🔑 API-Konfiguration

### Erforderliche API-Keys (.env)
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# APIs - WICHTIG: Verschiedene APIs für verschiedene Workflows!
OPENROUTER_API_KEY=your-key  # Für beide Workflows
SERPER_API_KEY=your-key      # NUR für AKTIVE Aufträge
COPYSCAPE_API_KEY=your-key   # Für beide Workflows  
DOCRAPTOR_API_KEY=your-key   # Für PDF-Export
```

## 📊 Workflow-Details

### OFFENE Aufträge (Bewerbungen)
- ✅ Titel wird automatisch generiert
- ❌ KEINE Serper API Nutzung
- 💰 Qualitätsstufen: Bronze ($0.35), Silber ($0.63), Gold ($0.93)
- 🎯 Fokus: Upwork-Job-Analyse und Arbeitsproben

### AKTIVE Aufträge (Kundenprojekte)
- ✅ Titel vom Kunden vorgegeben
- ✅ MIT Serper API für Research
- 📅 Wöchentliche Organisation
- 🎯 Fokus: Hochwertige Scripts für Kunden

## 🛡️ Sicherheitsfeatures

- **Workflow-Validator**: Verhindert falsche API-Nutzung
- **Cost-Tracker**: Überwacht API-Kosten
- **Audit-Logging**: Protokolliert alle Workflow-Aktionen

## 🚀 Deployment

### Produktionseinstellungen
```bash
# .env für Produktion
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@localhost/pw_script_studio
```

### Mit Gunicorn
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## 📝 Entwicklung

### Tests ausführen
```bash
python manage.py test
```

### Neue Migration erstellen
```bash
python manage.py makemigrations app_name
```

### Admin-Interface
- URL: `http://localhost:8000/admin/`
- Login mit Superuser-Credentials

## 🤝 Beitragen

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Committe deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## ⚠️ Wichtige Hinweise

- **Workflow-Trennung ist kritisch!** OFFENE ≠ AKTIVE Aufträge
- Serper API nur für AKTIVE Aufträge verwenden
- API-Kosten im Auge behalten
- Environment-Variablen niemals committen

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) Datei für Details.

## 📞 Support

Bei Fragen oder Problemen:
- Issue erstellen: [GitHub Issues](https://github.com/[USERNAME]/PW-Script-Studio/issues)
- Dokumentation: [Wiki](https://github.com/[USERNAME]/PW-Script-Studio/wiki)

---

**PW-Script-Studio v1.0** - Professionelles Script-Management mit getrennten Workflows
