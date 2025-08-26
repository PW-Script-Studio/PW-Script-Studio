# 🚀 Schnelle GitHub Upload Anleitung

## ✅ Ihr Projekt ist bereit!

Das Git-Repository ist bereits initialisiert und alle Dateien sind committed.

## 📋 Einfache 3-Schritte Anleitung:

### Schritt 1: GitHub Repository erstellen (2 Minuten)
1. Öffnen Sie https://github.com/new
2. Repository Name: `PW-Script-Studio`
3. Beschreibung: `Django Script-Management-System mit getrennten Workflows`
4. Wählen Sie Public oder Private
5. ⚠️ WICHTIG: Lassen Sie alle Checkboxen LEER (kein README, .gitignore, License)
6. Klicken Sie "Create repository"

### Schritt 2: Ihr GitHub Username herausfinden
- Schauen Sie in die URL nach der Repository-Erstellung
- Es wird etwa so aussehen: `https://github.com/IHR-USERNAME/PW-Script-Studio`
- Merken Sie sich `IHR-USERNAME`

### Schritt 3: Code hochladen (1 Minute)
Führen Sie diese Befehle in Ihrem Terminal aus:

```bash
# Ersetzen Sie IHR-USERNAME mit Ihrem echten GitHub-Username
git remote add origin https://github.com/IHR-USERNAME/PW-Script-Studio.git
git branch -M main
git push -u origin main
```

## 🔐 Authentifizierung
Beim ersten Push werden Sie gefragt:
- **Username**: Ihr GitHub-Username
- **Password**: Ihr GitHub-Personal Access Token

### Personal Access Token erstellen (falls nötig):
1. GitHub → Settings → Developer settings → Personal access tokens
2. "Generate new token" → "Generate new token (classic)"
3. Wählen Sie `repo` scope
4. Kopieren Sie das Token und verwenden Sie es als Passwort

## 🎉 Fertig!
Nach erfolgreichem Push ist Ihr Projekt online unter:
`https://github.com/IHR-USERNAME/PW-Script-Studio`

---

**Das war's! Ihr professionelles Django-Projekt ist jetzt auf GitHub! 🚀**
