- HauptDashboardmodultool mit moderner und optisch hochwertiger vollmodularer GUI
- Globale Standards, best practices und Manifeste implementieren
- perfekt ausgearbeitete auf Laien verwendung optimierte Hilfe und Führung im Tool
- Vollautomatische erstellung einer virtuellen Umgebung mit prüfung und auflösung von abhängigkeiten mit nutzerfeedback
- Entwicklerdokumentation
- Vallidierung aller eingangs und ausgangsfunktionen und daten
- sehr informatives und übersichtliches Dashboard mit hilfreichen statistika, anzeige datum uhrzeit und allgemeinen einstellungen, logging in echtzeit und tips sowie Uhrzeit und datum und speicherort.
- Hoch perfektionierte Darstellung, Flexibilität aller Größen und Positionen der Fenster
- Debuggingmodul für detailiertes logging und test, sowie problemlösungen die man durch drücken von buttons auslösen kann
- navigation über tastatur ermöglichen
- vollautomatische test implementieren
- selfrepair und intelligentes fehler handling
- maximal gute sichtbarkeit und farbwahl mit vier unterschiedlichen Farbthemes mit modernem Aussehen.
- Ansicht auch auf kleineren Bildschirmen ermöglichen
- Dynamische Anpassungen der Elemente und Fenster
- Linke aufklappbare sidebar zur anzeige vorhandener module
- professionelle analyse der besten Umsetzungen der GUI in bezug auf Optik, ansicht, darstellung, größe und farben
- Mockup und Logo mit erstellen
- infodatei mit verzeichnis und dateistruktur
- Maximale konfiguration und optionen im tool und alles über die GUI einstellbar
- Hauptfenster steuert untermodule, die sind maximierbar, deaktivierbar und ablösbar vom Hauptfenster
- Notizbereich der persistent notizen speichert im Dashboard
- autospeichern bei feldwechel und alle zehn minuten und beim schließen
- Alle funktionen prüfen vorher auf vorhandensein, bei fehlen korrigiert tool selbstständig
- detailierte fehlerbenennung, auch für laien verständlich mit auswahl einer Lösung über buttons

---

## PROVOWARE GLOBAL DEVELOPMENT CONTRACT

Dieser globale Kern gilt zusätzlich zu den projektspezifischen Regeln. Bei Sicherheits- oder Nachvollziehbarkeitskonflikten hat er Vorrang; lokale Regeln dürfen ihn verschärfen, nicht stillschweigend abschwächen.

- **Frozen Current Plan:** Laufenden freigegebenen Plan nicht durch neue Ideen erweitern; Neues in die nächste Iteration einordnen.
- **Conflict Gate:** Unterbrechen nur bei nachgewiesenem Konflikt mit Planvoraussetzung, Sicherheit, Ausgangs-SHA, Scope oder Invariant.
- **Single Writer:** Pro produktivem Scope nur ein autorisierter Executor; Analyse/Planung/Prüfung dürfen parallel lesen.
- **SHA + Scope:** Vor Mutation HEAD und erlaubten/verbotenen Scope prüfen; keine stillen Nebenrefactorings.
- **Evidence:** Kein PASS ohne echten Test; Evidence muss zum geprüften HEAD gehören.
- **Controlled Evidence Lab:** Echte Mutationen, Fehler-Injektion und Recovery-Tests nur in isolierten Testbereichen; Produktivdaten bleiben geschützt.
- **Next Queue:** Neue Anforderungen/Findings append-only erfassen und Beziehungen wie BLOCKS, REQUIRES, SUPERSEDES, DUPLICATE oder CONFLICTS dokumentieren.
- **Statusklarheit:** OBSERVED/SUSPECTED/REPRODUCED/CONFIRMED/DISPROVED nicht vermischen.
- **Recovery Key:** Nach Abbruch oder Agentenwechsel müssen Stand, Ziel, Frozen Plan, Scope, Findings, Gates und nächster erlaubter Schritt ohne alten Chat rekonstruierbar sein.
- **Traceability:** Requirement/Decision → Finding → Plan → Change → Test/Evidence → Gate/Checkpoint nachvollziehbar halten.
- **Negativtests:** Schutzmechanismen absichtlich gegen falschen SHA, zweiten Writer, Scope-Verstoß und unbelegtes PASS testen.
- **Sichtbarer Fortschritt:** Längere Prüfungen mit Schritt, Fortschritt, Ergebnis und Ampelstatus darstellen.

Leitsatz: **Kein Agent muss sich erinnern. Kein Agent darf raten. Keine Änderung verliert ihren Ursprung. Kein PASS existiert ohne Evidence.**
