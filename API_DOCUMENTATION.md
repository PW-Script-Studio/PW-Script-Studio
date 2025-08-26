# 🚀 PW-Script-Studio REST API Documentation

## 📍 Base URL
```
http://127.0.0.1:8000/api/
```

## 🔧 Available Endpoints

### 1. **Aufträge (Auftrag Model)**

#### **GET /api/auftraege/**
Alle Aufträge abrufen
```json
{
  "count": 3,
  "results": [
    {
      "id": "UW-2025-001",
      "titel": "Upwork Bewerbung - Content Writer",
      "status": "OFFEN",
      "prioritaet": "HOCH",
      "woche": 4,
      "is_offen": true,
      "is_aktiv": false,
      "arbeitsproben_count": 1,
      "scripts_count": 0
    }
  ]
}
```

#### **GET /api/auftraege/offene/**
Nur OFFENE Aufträge (Bewerbungen)
```json
{
  "count": 2,
  "workflow": "OFFEN",
  "description": "Bewerbungen - Titel wird generiert, KEINE Serper API",
  "auftraege": [...]
}
```

#### **GET /api/auftraege/aktive/**
Nur AKTIVE Aufträge (Kundenprojekte)
```json
{
  "count": 1,
  "workflow": "AKTIV", 
  "description": "Kundenprojekte - Titel vom Kunden, MIT Serper API",
  "auftraege": [...]
}
```

#### **GET /api/auftraege/dashboard_stats/**
Dashboard-Statistiken
```json
{
  "total_auftraege": 3,
  "offene_auftraege": 2,
  "aktive_auftraege": 1,
  "abgeschlossene_auftraege": 0,
  "total_arbeitsproben": 1,
  "total_scripts": 1,
  "api_kosten_gesamt": "0.93",
  "serper_kosten_gesamt": "0.02",
  "neueste_auftraege": [...]
}
```

### 2. **Arbeitsproben (OFFENE Aufträge)**

#### **GET /api/arbeitsproben/**
Alle Arbeitsproben abrufen
- Query Parameter: `?auftrag=UW-2025-001` (Filter nach Auftrag)

#### **GET /api/arbeitsproben/by_quality/**
Arbeitsproben gruppiert nach Qualität
```json
{
  "bronze": {
    "count": 0,
    "total_cost": 0,
    "arbeitsproben": []
  },
  "gold": {
    "count": 1,
    "total_cost": "0.93",
    "arbeitsproben": [...]
  }
}
```

#### **POST /api/arbeitsproben/**
Neue Arbeitsprobe erstellen
```json
{
  "auftrag": "UW-2025-001",
  "generated_title": "Professioneller Content Writer",
  "content": "Bewerbungstext...",
  "quality": "gold"
}
```

### 3. **Scripts (AKTIVE Aufträge)**

#### **GET /api/scripts/**
Alle Scripts abrufen
- Query Parameter: `?auftrag=KD-2025-001` (Filter nach Auftrag)
- Query Parameter: `?week=4` (Filter nach Woche)

#### **GET /api/scripts/by_week/**
Scripts gruppiert nach Wochennummer
```json
[
  {
    "week_number": 4,
    "count": 1,
    "total_serper_calls": 1,
    "total_serper_cost": "0.02"
  }
]
```

#### **POST /api/scripts/{id}/add_serper_call/**
Serper API Call hinzufügen
```json
{
  "cost": 0.01
}
```

Response:
```json
{
  "message": "Serper API Call hinzugefügt",
  "serper_api_calls": 2,
  "serper_kosten": "0.03"
}
```

## 🎯 Workflow-Logik

### **OFFENE Aufträge (Bewerbungen)**
- ✅ Titel wird **GENERIERT** (nicht vom Kunden)
- ✅ **KEINE** Serper API Nutzung
- ✅ Fokus auf **Qualitätsstufen** (Bronze/Silber/Gold)
- ✅ **API-Kosten** basierend auf Qualität

### **AKTIVE Aufträge (Kundenprojekte)**
- ✅ Titel vom **KUNDEN** vorgegeben
- ✅ **MIT** Serper API für Research
- ✅ Fokus auf **wöchentliche Organisation**
- ✅ **Serper-Kosten** Tracking

## 🔐 Authentication
Aktuell keine Authentication erforderlich (Development).
Für Production: Django REST Framework Token Authentication.

## 📊 Status Codes
- **200**: OK
- **201**: Created
- **400**: Bad Request
- **404**: Not Found
- **500**: Internal Server Error
