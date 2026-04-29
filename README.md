# Monte-Carlo-Simulation eines kleinen Eisgeschaefts

## Aufgabenstellung

Dieses Projekt ist ein kleiner Teilbeleg fuer das Fach "Diskrete Simulation". Untersucht wird ein kleines Eisgeschaeft mit zufaellig ankommenden Kunden und zufaelligen Bestellungen. Mit Hilfe einer Monte-Carlo-Simulation soll abgeschaetzt werden, welcher durchschnittliche Jahresgewinn entstehen kann.

Die Hauptfrage lautet:

**Wie hoch ist der durchschnittliche Jahresgewinn des Eisgeschaefts unter den gewaehlten Annahmen?**

Zusaetzlich wird untersucht, welche Eissorten am haeufigsten verkauft werden. Dadurch kann der Geschaeftsleiter erkennen, welche Sorten im Modell besonders wichtig sind.

## Bezug zur Monte-Carlo-Methode aus Vorlesung und Praktikum

Das Modell orientiert sich am typischen Ablauf einer Monte-Carlo-Simulation aus Vorlesung und Praktikum:

1. Es werden Eingabeparameter festgelegt.
2. Zufallszahlen erzeugen moegliche Ereignisse.
3. Ein Jahr wird Tag fuer Tag simuliert.
4. Die Simulation wird viele Male wiederholt.
5. Aus den Wiederholungen werden Durchschnittswerte berechnet.

Im Programm werden dafuer einfache Schleifen, Zufallszahlen, Zaehler und Mittelwerte verwendet. Ein Monte-Carlo-Lauf entspricht einem simulierten Jahr mit 365 Tagen.

## Modellannahmen

Das Eisgeschaeft hat im Modell jeden Tag im Jahr geoeffnet. Fuer jeden Tag wird zuerst der Monat bestimmt. Danach wird eine zufaellige Temperatur erzeugt. Die Temperaturbereiche sind einfache angenommene Monatswerte, zum Beispiel 0 bis 8 Grad im Januar und 19 bis 34 Grad im Juli.

Die Kundenzahl haengt von der Temperatur ab. Bei kaltem Wetter kommen weniger Kunden, bei warmem Wetter kommen mehr Kunden. Zusaetzlich wird eine zufaellige Schwankung zwischen 0,8 und 1,2 verwendet.

Jeder Kunde kauft zufaellig 1, 2 oder 3 Kugeln. Die Wahrscheinlichkeiten fuer die Portionsgroesse haengen ebenfalls von der Temperatur ab. Bei hoeheren Temperaturen sind groessere Portionen wahrscheinlicher.

Fuer jede einzelne Kugel wird eine Eissorte zufaellig ausgewaehlt. Die Sorten werden gewichtet:

| Eissorte | Gewicht |
| --- | ---: |
| Vanille | 22 |
| Schokolade | 20 |
| Erdbeere | 18 |
| Zitrone | 14 |
| Stracciatella | 14 |
| Pistazie | 12 |

## Zufallsgroessen

Im Modell werden folgende Zufallsgroessen verwendet:

- Temperatur pro Tag
- zufaellige Schwankung der Kundenzahl
- Portionsgroesse pro Kunde
- Eissorte pro verkaufter Kugel

Die Temperatur ist der zeitabhaengige Basisparameter, weil sie sich ueber die Monate des Jahres veraendert.

## Zielfunktion

Die Zielfunktion ist der maximale durchschnittliche Jahresgewinn:

`maximiere durchschnittlichen Jahresgewinn`

Die Berechnung erfolgt mit:

- `Tagesumsatz = verkaufte Kugeln * Preis pro Kugel`
- `variable Kosten = verkaufte Kugeln * Kosten pro Kugel`
- `Tagesgewinn = Tagesumsatz - variable Kosten - Fixkosten pro Tag`
- `Jahresgewinn = Summe aller Tagesgewinne`

Nach vielen Monte-Carlo-Laeufen wird der durchschnittliche Jahresgewinn berechnet.

## Bewertungsparameter

Die Webanwendung zeigt folgende Werte:

- durchschnittlicher Jahresgewinn
- durchschnittlicher Jahresumsatz
- durchschnittliche Kundenzahl pro Jahr
- durchschnittlich verkaufte Kugeln pro Jahr
- beliebteste Eissorte
- minimaler simulierter Jahresgewinn
- maximaler simulierter Jahresgewinn
- durchschnittlich verkaufte Kugeln pro Eissorte
- kurze Interpretation

## Bedienung lokal

Zuerst werden die Abhaengigkeiten installiert:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Danach startet man die Anwendung:

```bash
python app.py
```

Anschliessend wird im Browser geoeffnet:

```text
http://localhost:5000
```

## Bedienung mit Docker

Docker kann verwendet werden, damit die Anwendung reproduzierbar in einer gleichen Umgebung laeuft:

```bash
docker build -t eis-monte-carlo .
docker run --rm -p 5000:5000 eis-monte-carlo
```

Danach wird im Browser geoeffnet:

```text
http://localhost:5000
```

## Ergebnisse fuer den Bericht

Aus der Weboberflaeche sollten folgende Werte in den Bericht uebernommen werden:

- durchschnittlicher Jahresgewinn
- durchschnittlicher Jahresumsatz
- durchschnittliche Kundenzahl pro Jahr
- durchschnittlich verkaufte Kugeln pro Jahr
- beliebteste Eissorte
- minimaler und maximaler simulierter Jahresgewinn
- Tabelle oder Screenshot der verkauften Kugeln pro Eissorte
- Balkendiagramm der Eissorten

Die Werte koennen direkt aus der Ergebnisansicht kopiert oder als Screenshot in den Bericht eingefuegt werden.

## Export der Einzelläufe

Nach jeder Simulation wird zusätzlich eine CSV-Datei im Ordner `simulation_exports/` erstellt. Jeder Monte-Carlo-Lauf wird dabei als eine eigene Zeile gespeichert. Die Datei verwendet ein Semikolon als Trennzeichen und kann direkt mit Excel geöffnet werden.

Die CSV-Datei wird mit Semikolon als Trennzeichen und Komma als Dezimaltrennzeichen gespeichert, damit sie in deutschem Excel korrekt geöffnet wird.

Der Export hilft dabei, die Simulation genauer zu prüfen und bei Bedarf weitere Diagramme zu erstellen. Für den Bericht ist die CSV-Datei besonders nützlich als Anhang, weil die einzelnen Simulationsläufe nachvollziehbar dokumentiert sind.

## Hinweis zu den Daten

Alle Werte sind vereinfachte Annahmen. Es handelt sich nicht um echte Geschaeftsdaten. Das Modell dient zur Demonstration der Monte-Carlo-Methode und nicht als echte betriebswirtschaftliche Prognose.

## Bericht fuer den Leiter des Eisgeschaeftes

**Ersteller: Kirill Artemov, Matrikelnummer: XXXX**

### Aufgabenstellung

Ziel dieser Untersuchung ist es, ein kleines Eisgeschaeft mit Hilfe einer Monte-Carlo-Simulation zu analysieren. Dabei soll abgeschaetzt werden, wie hoch der durchschnittliche Jahresgewinn unter vereinfachten Annahmen ausfallen kann. Zusaetzlich soll untersucht werden, welche Eissorten im Modell besonders haeufig verkauft werden. Die Ergebnisse sollen dem Leiter des Eisgeschaeftes eine einfache Orientierung geben, welche wirtschaftliche Entwicklung unter den gewaehlten Modellannahmen moeglich ist.

### Modellannahmen

Das Geschaeft wird fuer ein vollstaendiges Jahr mit 365 Tagen betrachtet. Jeder Simulationslauf entspricht einem moeglichen Jahr. Fuer jeden Tag wird zunaechst der Monat bestimmt. Anschliessend wird aus einem monatlichen Temperaturbereich eine zufaellige Temperatur erzeugt. Dadurch wird beruecksichtigt, dass ein Eisgeschaeft im Sommer normalerweise mehr Kunden hat als im Winter.

Die Kundenzahl wird aus einer Basiskundenzahl von 25 Kunden pro Tag berechnet. Diese Basiskundenzahl wird mit einem Temperaturfaktor multipliziert. Bei Temperaturen unter 10 Grad wird nur ein Faktor von 0,4 verwendet. Zwischen 10 und 20 Grad gilt Faktor 0,8, zwischen 20 und 30 Grad Faktor 1,3 und ab 30 Grad Faktor 1,6. Zusaetzlich wird eine zufaellige Schwankung zwischen 0,8 und 1,2 einbezogen. Dadurch entstehen von Tag zu Tag unterschiedliche Kundenzahlen.

Jeder Kunde kauft zufaellig eine Portion mit 1, 2 oder 3 Kugeln. Auch hier haengt die Wahrscheinlichkeit von der Temperatur ab. An kalten Tagen werden meistens kleine Portionen gekauft. An warmen Tagen steigen die Wahrscheinlichkeiten fuer zwei oder drei Kugeln. Fuer jede einzelne Kugel wird danach eine Eissorte ausgewaehlt. Dabei werden die Sorten Vanille, Schokolade, Erdbeere, Zitrone, Stracciatella und Pistazie mit festen Gewichtungen beruecksichtigt.

### Zielfunktion

Die wirtschaftliche Zielgroesse ist der durchschnittliche Jahresgewinn. Der Tagesumsatz ergibt sich aus der Anzahl der verkauften Kugeln multipliziert mit dem Preis pro Kugel. Von diesem Umsatz werden die variablen Kosten pro Kugel und die taeglichen Fixkosten abgezogen. Die Summe aller Tagesgewinne ergibt den Jahresgewinn. Da ein einzelnes simuliertes Jahr zufallsabhaengig ist, wird die Simulation viele Male wiederholt. Die Zielfunktion lautet daher: Maximierung des durchschnittlichen Jahresgewinns ueber alle Monte-Carlo-Laeufe.

### Ergebnisse

Bei der Durchfuehrung der Simulation mit den gewaehlten Eingabewerten ergab sich ein durchschnittlicher Jahresgewinn von [durchschnittlichen Jahresgewinn aus der Simulation einfuegen]. Der durchschnittliche Jahresumsatz betrug [durchschnittlichen Jahresumsatz aus der Simulation einfuegen]. Pro Jahr kamen im Durchschnitt [durchschnittliche Kundenzahl aus der Simulation einfuegen] Kunden in das Geschaeft. Insgesamt wurden durchschnittlich [durchschnittlich verkaufte Kugeln aus der Simulation einfuegen] Kugeln pro Jahr verkauft.

Der kleinste simulierte Jahresgewinn lag bei [minimalen Jahresgewinn aus der Simulation einfuegen], waehrend der groesste simulierte Jahresgewinn [maximalen Jahresgewinn aus der Simulation einfuegen] betrug. Die beliebteste Eissorte in der Simulation war [beliebteste Eissorte aus der Simulation einfuegen]. Die Tabelle und das Balkendiagramm der Webanwendung zeigen ausserdem, wie sich die verkauften Kugeln auf die einzelnen Sorten verteilen.

### Interpretation

Die Ergebnisse zeigen, dass der wirtschaftliche Erfolg des Eisgeschaeftes stark von der Temperatur und damit von der Saison abhaengt. In warmen Monaten entstehen mehr Kundenkontakte und gleichzeitig werden groessere Portionen wahrscheinlicher. Dadurch steigen Umsatz und Gewinn besonders in den Sommermonaten. In kalten Monaten ist die Kundenzahl dagegen niedriger, waehrend die Fixkosten weiterhin anfallen. Das kann den Jahresgewinn deutlich belasten.

Die Auswertung der Eissorten zeigt, welche Sorten im Modell besonders stark nachgefragt werden. Da die Sorten mit festen Gewichtungen ausgewaehlt werden, liegen Vanille, Schokolade und Erdbeere meistens weit vorne. Trotzdem koennen die genauen Werte zwischen einzelnen Simulationsdurchlaeufen leicht schwanken, weil jede Kugel zufaellig einer Sorte zugeordnet wird. Fuer den Geschaeftsleiter kann diese Information hilfreich sein, um die wichtigsten Sorten bei der Planung des Angebots besonders zu beachten.

### Grenzen des Modells

Das Modell ist bewusst einfach gehalten. Es verwendet keine echten Wetterdaten und keine echten Verkaufsdaten. Auch Feiertage, Wochenenden, Ferien, Personalplanung, Lagerhaltung, Verderb, Konkurrenz und besondere Aktionen werden nicht beruecksichtigt. Ausserdem wird angenommen, dass das Geschaeft jeden Tag im Jahr geoeffnet ist. Die Ergebnisse sollten deshalb nicht als genaue Prognose verstanden werden, sondern als einfache Simulation zur Untersuchung grundsaetzlicher Zusammenhaenge.

### Fazit

Die Monte-Carlo-Simulation zeigt anschaulich, wie sich zufaellige Temperaturen, Kundenzahlen, Portionsgroessen und Sortenwahlen auf den Jahresgewinn eines kleinen Eisgeschaeftes auswirken koennen. Besonders wichtig ist die Abhaengigkeit von der Saison. Die Simulation liefert Durchschnittswerte und eine einfache Spannweite zwischen minimalem und maximalem simulierten Jahresgewinn. Fuer eine reale Entscheidung muesste das Modell mit echten Daten erweitert werden. Fuer den Zweck des Teilbelegs zeigt es jedoch nachvollziehbar, wie eine Monte-Carlo-Simulation fuer ein diskretes System aufgebaut und ausgewertet werden kann.
