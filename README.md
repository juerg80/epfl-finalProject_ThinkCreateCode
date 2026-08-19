# Bike Messenger Simulation

Eine kleine Flask-Webanwendung, in der eine Fahrradkurier-Firma über mehrere
Schichten geführt wird. Ziel ist es, möglichst viel Geld zu erwirtschaften,
indem Aufträge passenden Fahrern zugewiesen werden. Wetter, Verkehrsbussen,
Fahrradprobleme, Zuverlässigkeit und Arbeitsauslastung sorgen für ein
zufallsabhängiges Spielerlebnis.

## Voraussetzungen

- Python 3.8 oder neuer
- Flask
- NumPy

Die Python-Abhängigkeiten können beispielsweise so installiert werden:

```bash
python -m pip install flask numpy
```

## Projektstruktur

| Datei | Zweck |
| --- | --- |
| `messenger_simul_main.py` | Flask-Anwendung und HTTP-Routen |
| `messenger_classes.py` | Spielregeln, Datenmodelle, Zufallsereignisse und Berechnungen |
| `index.html` | Hauptseite und Spielablauf |
| `assignment.html` | Auftragszuweisung an die verfügbaren Fahrer |
| `ShowRiders.html` | Fahrerübersicht |
| `ShowMap.html` | Distanz- und Höhenkarten |
| `ShowStats.html` | Statistiken der letzten Schicht |
| `config_base.txt` | Startkapital, Fahrer, Wetter- und Auftragsparameter |
| `map_distances.txt` | Distanzmatrix zwischen den Orten |
| `map_altitudes.txt` | Höhen- beziehungsweise Steigungsmatrix |
| `static/` | CSS und JavaScript für die Benutzeroberfläche |

## Einrichtung

Vor dem ersten Start müssen in `messenger_simul_main.py` die drei Variablen
`config_File`, `map_distances_file` und `map_altitudes_file` angepasst werden.
Im Ausgangszustand enthalten sie absolute Windows-Pfade aus der
Entwicklungsumgebung des Projekts. Verwende für eine lokale Kopie die Pfade
zu den Dateien im Repository, zum Beispiel:

```python
config_File = "config_base.txt"
map_distances_file = "map_distances.txt"
map_altitudes_file = "map_altitudes.txt"
```

Relative Pfade funktionieren, wenn die Anwendung aus dem Projektverzeichnis
gestartet wird.

## Anwendung starten

Im Projektverzeichnis:

```bash
python messenger_simul_main.py
```

Danach die von Flask ausgegebene lokale Adresse im Browser öffnen. Falls kein
Server gestartet wird, ergänze am Ende von `messenger_simul_main.py` einen
Flask-Startpunkt oder starte die Anwendung über einen geeigneten WSGI-Server.

## Spielablauf

1. **Init Game** auswählen. Dadurch werden Karte, Fahrer, Startkapital und der
   Anfangszustand geladen.
2. **Next Shift** auswählen. Die nächste Schicht erzeugt zufällige Aufträge,
   bestimmt das Wetter und zeigt die verfügbaren Fahrer.
3. Auf der Zuweisungsseite pro Fahrer die Nummern der Aufträge eintragen.
   Mehrere Aufträge werden mit einem Semikolon getrennt, zum Beispiel `2;1`.
   Die Reihenfolge entspricht der geplanten Ausführungsreihenfolge.
4. `0` eintragen, wenn ein Fahrer keinen Auftrag erhalten soll.
5. **Apply Assignment** auswählen. Die Anwendung prüft die Eingabe und bucht
   Löhne, Einnahmen, Bussen und allfällige Strafzahlungen.
6. Über **Show Stats Last Shift**, **Show Riders** und **Show Map** können die
   Ergebnisse und die aktuellen Spieldaten eingesehen werden.
7. Mit **Next Shift** die Simulation fortsetzen.

Ein Auftrag darf höchstens einem Fahrer zugewiesen werden. Nicht jeder
Auftrag muss zugewiesen werden, nicht zugewiesene Aufträge verursachen jedoch
eine von `PenaltyMissedOrder` abhängige Strafe. Sobald das aktuelle Guthaben
negativ ist, ist das Spiel beendet.

## Konfiguration

`config_base.txt` ist eine einfache Schlüssel-Wert-Datei im Format
`Schlüssel:Wert`. Wichtige Parameter sind:

- `Cash`: Startguthaben
- `NumberRiders`: Anzahl konfigurierter Fahrer
- `f1_*`, `f2_*`, ...: Name, Geschwindigkeit, Lohn, Auslastung und
  Zuverlässigkeit der Fahrer
- `map1`: Orte, die in der Karte verwendet werden
- `AnzOrder_lambda`: Erwartungswert der zufälligen Auftragsanzahl
- `VolumeOrder_*`: Parameter für das Auftragsvolumen
- `weather` und `weather_probas`: mögliche Wetterlagen und ihre Wahrscheinlichkeiten
- `mean_fine_per_rider_and_shift` und `std_fine_per_rider_and_shift`:
  Verkehrsbussen pro Fahrer und Schicht
- `bike_issue_probas`: Wahrscheinlichkeiten für Fahrradereignisse

Die beiden Matrixdateien müssen numerische Tabellen enthalten. Ihre Zeilen
und Spalten müssen zur Reihenfolge der Orte in `map1` passen.

## Verfügbare Routen

| Route | Funktion |
| --- | --- |
| `/` | Hauptseite |
| `/init` | Neues Spiel initialisieren |
| `/PrepareNextShift` | Aufträge für die nächste Schicht erzeugen |
| `/GetRiderAssignment` | Zuordnung verarbeiten |
| `/ShowStats` | Statistiken anzeigen |
| `/ShowRiders` | Fahrer anzeigen |
| `/ShowMap` | Kartenmatrizen anzeigen |

## Entwicklung und Tests

Das Projekt enthält derzeit keine automatisierte Test-Suite. Ein schneller
Syntaxcheck für die Python-Dateien ist:

```bash
python -m py_compile messenger_classes.py messenger_simul_main.py
```

Für einen manuellen Funktionstest sollte die Anwendung gestartet, ein Spiel
initialisiert, mindestens eine Schicht erzeugt und eine gültige sowie eine
ungültige Auftragszuweisung ausprobiert werden.

## Bekannte Einschränkungen

- Die Dateipfade in `messenger_simul_main.py` sind derzeit nicht automatisch
  plattformunabhängig.
- Die Anwendung speichert Spielzustände nur im Prozessspeicher; ein Neustart
  setzt das Spiel zurück.
- Zufallswerte werden nicht mit einem festen Seed initialisiert. Ergebnisse
  unterscheiden sich daher zwischen den Durchläufen.
- Es gibt keine Benutzerverwaltung und keine persistente Highscore-Datenbank.

## Lizenz

Im Repository ist derzeit keine separate Lizenzdatei enthalten.