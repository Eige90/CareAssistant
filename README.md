# CareAssistant 0.6

## Änderungen

### Kalender
- Monatsansicht vollständig neu aufgebaut
- Milchglas-Kacheln mit höherem Schwarz-/Weißanteil für bessere Lesbarkeit
- Ereignisse werden direkt im jeweiligen Kalendertag angezeigt
- bis zu drei Ereignisse pro Tag sichtbar, weitere Termine werden zusammengefasst
- Tages- und Wochenansicht zeigen gespeicherte Ereignisse weiterhin an

### Profil
- kein separater Button zum Entfernen des Profilbildes
- Entfernen nur noch über ein `×` am runden Profilbild beim Hover
- `×` liegt vollständig innerhalb des Profilbereichs
- Profilmenü enthält jetzt zusätzlich `Abmelden`
- Abmelden wechselt in eine lokale abgemeldete Sitzung; es ist noch kein Passwort-/Server-Login

### Über CareAssistant
- zeigt aktuell ausschließlich Version und Autor

### Modul Betreute
Erste funktionsfähige Version der digitalen Betreutenakte:

- Suche nach Name und Aktenzeichen
- Liste aller Betreuten mit Status
- Betreuten anlegen und bearbeiten
- Stammdaten
  - Vorname / Nachname
  - Geburtsdatum
  - Anschrift
  - Telefon / E-Mail mit Validierung
- Betreuungsfall
  - Betreuungsgericht
  - Aktenzeichen
  - Beginn der Bestellung
  - Status: Aktiv / Ruhend / Beendet
  - Aufgabenbereiche
- Versorgung
  - Krankenkasse
  - Pflegegrad
  - GdB
- interne Notizen
- Übersichtskarten für Stammdaten, Betreuungsfall, Aufgabenbereiche und Versorgung
- lokale persistente Speicherung

## Start

```powershell
cd CareAssistant_v0.6
pip install -r requirements.txt
python main.py
```

## Hinweis zum Entwicklungsstand

Die lokale Speicherung ist für die Entwicklung gedacht. Bevor CareAssistant mit echten Betreutendaten produktiv eingesetzt oder veröffentlicht wird, müssen Datenschutz, Zugriffsschutz, Backups und eine geeignete Verschlüsselung der gespeicherten Daten separat umgesetzt und geprüft werden.
