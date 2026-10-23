> **Website / Projektseite:** [CareAssistant](https://eige90.github.io/CareAssistant/) · Projektbeschreibung und lokale Startanleitung.

# CareAssistant v0.6

**Source version / Version im Code:** `v0.6.0`

## English

A local desktop application for organizing appointments and case information in legal guardianship workflows. Built with Python and PySide6.

### Start (Windows PowerShell)

```powershell
git clone https://github.com/Eige90/CareAssistant.git
cd CareAssistant
python -m pip install -r requirements.txt
python main.py
```

Requires Python 3 and the dependencies listed in `requirements.txt`.

### Current features
- Calendar with month, week, and day views and visible events
- Appointment details and locally stored events
- Client records with search, case references, guardianship status, contact details, and notes
- Profile and appearance settings
- Local persistence

### Development and privacy
Version 0.6 is a development build. The local signed-out screen is **not** a secure server-backed authentication system. Do not use real sensitive client records in production without appropriate access controls, encryption, backups, and a data-protection review.

---

## Roadmap / Open verification items

- [ ] Verify calendar layout, event-detail dialogs, navigation and remaining v0.6 UI issues.
- [ ] Verify client autocomplete accepts both existing and new entries.
- [ ] Before real client data: add authentication, access control, encryption, backups and a privacy review.


## Deutsch

Eine lokale Desktop-Anwendung zur Terminplanung und Verwaltung von Betreuungsakten. Entwickelt mit Python und PySide6.

### Start (Windows PowerShell)

```powershell
git clone https://github.com/Eige90/CareAssistant.git
cd CareAssistant
python -m pip install -r requirements.txt
python main.py
```

Benötigt Python 3 und die Pakete aus `requirements.txt`.

### Aktueller Funktionsumfang
- Kalender mit Monats-, Wochen- und Tagesansicht und sichtbaren Terminen
- Termindetails und lokale Terminspeicherung
- Betreutenakten mit Suche, Aktenzeichen, Status, Kontaktdaten und Notizen
- Profil- und Design-Einstellungen
- Lokale persistente Speicherung

### Entwicklungsstand und Datenschutz
Version 0.6 befindet sich in Entwicklung. Die lokale Abmeldeansicht ist **keine** sichere serverbasierte Anmeldung. Echte sensible Betreutendaten sollten erst nach Umsetzung geeigneter Zugriffsrechte, Verschlüsselung, Backups und Datenschutzprüfung produktiv verarbeitet werden.

---

Built by [Eige90](https://github.com/Eige90).

## Roadmap / Offene Prüfpunkte

- [ ] Kalenderlayout, Termindetails, Navigation und offene UI-Punkte aus v0.6 überprüfen.
- [ ] Autovervollständigung bei Betreuten prüfen; unbekannte Eingaben weiterhin zulassen.
- [ ] Vor Einsatz mit Echtdaten: Anmeldung, Zugriffsschutz, Verschlüsselung, Backups und Datenschutz prüfen.


## GitHub Pages / Website status

**English:** Python/PySide6 desktop application: GitHub Pages cannot host the running app; a documentation site would be separate.

**Deutsch:** Python/PySide6-Desktop-App: GitHub Pages kann die Anwendung nicht ausführen; eine Dokumentationsseite wäre ein separates Angebot.
