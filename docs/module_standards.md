# Modul-Standards

Alle neuen Module müssen sich an die Vorgaben des Hauptmodultools halten, damit
Bedienung und Optik konsistent bleiben.

## Layout- und Größenrichtlinien
- Mindestbreite: 320px, Mindesthöhe: 240px.
- Innenabstand ("Padding": Innenabstand) beträgt 16px.
- Module sollen Tastenkürzel ("Tastenkürzel": kurze Tastenfolge) für Fokus, Sichtbarkeit
  und Ablösen anbieten (siehe `ModuleStandard.keyboard_shortcuts`).
- Seitenleiste ("Sidebar": Seitenleiste) nutzt 22% der Gesamtbreite. Auf kleineren
  Bildschirmen darf sie einklappen.
- Nutze die Breakpoints ("Breakpoint": Umschaltpunkt) aus `ResponsiveLayoutProfile`
  für mobile, Tablet-, Desktop- und Wide-Layouts.

## Farb- und Sichtbarkeitskonzept
- Wähle eines der vier definierten Themes (`aurora`, `sunrise`, `forest`, `monochrome`).
- Primär- und Sekundärfarben müssen WCAG-Kontraststufen von mindestens 4.5:1 erfüllen.
- Texte setzen `text_primary` für Hauptinhalte und `text_secondary` für Meta-Informationen.

## Barrierefreiheit und Bedienung
- Alle interaktiven Elemente müssen über die Tastatur erreichbar sein.
- Tooltips erklären Fachbegriffe sofort in einfachen Worten.
- Fehlermeldungen enthalten eine laienverständliche Problembeschreibung sowie Buttons für
  automatische Lösungsvorschläge.

## Speicher- und Autosave-Vorgaben
- Autosave löst bei Feldwechsel, Timer (alle 10 Minuten) und beim Schließen aus.
- Daten werden im Pfad `var/data` abgelegt; Unterordner pro Modul.
- Bei fehlenden Daten versucht das Modul eine Selbstheilung (z.B. Standarddatei anlegen).
- Logdateien ("Logdatei": Textdatei mit Meldungen) liegen unter `var/log/dashboardtool`
  und müssen im JSON-Zeilen-Format gespeichert werden, damit sie maschinenlesbar
  und für Laien verständlich kommentiert sind.
