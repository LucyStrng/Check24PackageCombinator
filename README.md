# Streaming Package Comparator 

## Projektbeschreibung
Das Streaming Package Comparator-Projekt ist eine Webanwendung, die es Nutzern ermöglicht, Wettbewerbe und Spiele zu analysieren und die günstigsten Streaming-Angebote basierend auf ihren Präferenzen zu vergleichen. 

Die Anwendung verwendet FastAPI als Backend, React für das Frontend und SQLAlchemy für die Datenbankverarbeitung.
---

## Features
### Frontend
- Anzeige von Wettbewerben in einer Tabelle mit mehreren Spalten für Streaming-Pakete.
- Ein- und Ausklappbare Details:
    - Spiele innerhalb eines Wettbewerbs können ein- und ausgeklappt werden.
- Paginierung:
-   Die Tabelle unterstützt mehrere Seiten

### Backend
Das Backend bietet mehrere API-Endpunkte, die folgende Funktionalitäten ermöglichen:

### **Spiele (Games)**
- **Abruf aller Spiele**:
  - **Methode**: `GET`
  - **Pfad**: `/`
  - **Beschreibung**: Gibt eine Liste aller verfügbaren Spiele zurück, einschließlich Team-Informationen und Turnierdetails.

---

### **Streaming-Pakete (Streaming Packages)**
- **Abruf aller Pakete**:
  - **Methode**: `GET`
  - **Pfad**: `/`
  - **Beschreibung**: Gibt eine Liste aller verfügbaren Streaming-Pakete zurück.
- **Abruf von Teams in Paketen**:
  - **Methode**: `GET`
  - **Pfad**: `/teams`
  - **Beschreibung**: Gibt eine Liste von Teams zurück, die in den verfügbaren Paketen unterstützt werden.
- **Ranking von Paketen**:
  - **Methode**: `GET`
  - **Pfad**: `/ranked`
  - **Beschreibung**: Gibt die Pakete in einer priorisierten Reihenfolge basierend auf ihren Eigenschaften zurück.
- **Optimalste Kombination von Paketen**:
  - **Methode**: `GET`
  - **Pfad**: `/optimal-combination`
  - **Beschreibung**: Berechnet die günstigste Kombination von Paketen, die alle Spiele abdeckt.

---

### **Vergleiche (Comparison)**
- **Vergleichsdaten abrufen**:
  - **Methode**: `GET`
  - **Pfad**: `/`
  - **Beschreibung**: Liefert Wettbewerbs-, Spiele- und Paketdaten in einer strukturierten Antwort.

---

## Voraussetzungen
### Systemanforderungen
- Python >= 3.8
- Node.js >= 14.x
- PostgreSQL oder SQLite für die Datenbank

### Installierte Bibliotheken
#### Backend
- FastAPI
- SQLAlchemy
- uvicorn

#### Frontend
- React
- Axios

---

## Setup-Anleitung

### Backend installieren
1. Klone das Repository:
   ```bash
   git clone 
   cd repository/backend
2. Python-Umgebung einrichten: 
    ```python -m venv venv
    source venv/bin/activate  # Für Linux/Mac
    venv\Scripts\activate     # Für Windows
    pip install -r requirements.txt
3. Datenbankinitialisieren 
    ```bash
    python load_data.py
4. Backend starten 
   ```bash 
   uvicorn app.main:app --reload
### Frontend installieren 
1. Frontend-Verzeichnis betreten:
   ```bash
   cd ../frontend
2. Abhängigkeiten installieren: 
    ```bash
    npm install 
3. React-Anwendung starten: 
    ```bash
    npm start 
Öffne die Anwendung im Browser: 
```
http://localhost:3001