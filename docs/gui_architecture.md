# GUI-Architektur und Mockup

Die folgende Beschreibung dient als leicht verständlicher Leitfaden für den
Aufbau der Benutzeroberfläche. Sie ergänzt `README.md` und zeigt, wie Sidebar,
Module und Hilfselemente zusammenspielen.

```
┌─────────────────────────────────────────────────────────────────────┐
│ Header: "DashboardTool" – Untertitel erklärt Zweck in Alltagssprache│
├─────────────┬───────────────────────────────────────────────────────┤
│ Sidebar     │ Hauptbereich                                         │
│ [Notes]     │  ┌───────────────┐  ┌─────────────────────────────┐  │
│ [Diagnose]  │  │ Notizbereich  │  │ Diagnose                    │  │
│ ...         │  │ Autosave-Hinw.│  │ Live-Logs + Filter          │  │
│             │  └───────────────┘  └─────────────────────────────┘  │
├─────────────┴───────────────────────────────────────────────────────┤
│ Footer: Status (Autosave, Uhrzeit, Speicherpfade)                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Kernelemente

- **Sidebar**: Klappbar, zeigt alle Module mit Kurzbeschreibung und Tastenkürzel
  ("Tastenkürzel": kurze Tastenfolge) an.
- **Module**: Werden als "Tiles" mit Metadaten, Layoutvorgaben und Aktionen
  durch `DashboardApp.render()` bereitgestellt.
- **Statuszeile**: Enthält Uhrzeit, aktive Autosave-Informationen und
  Speicherorte, damit Laien nachvollziehen können, wo Daten liegen.
- **Themes**: Vier vorkonfigurierte Farbwelten mit Kontrastbericht, damit auch
  ohne Fachwissen ein gutes Design gewählt werden kann.

## Logo-Idee

Als Basis-Logo eignet sich ein stilisiertes Dashboard-Symbol:

- Hintergrund: Kreis mit Verlauf von `#5bc0be` zu `#2b59c3`.
- Vordergrund: Vier Quadranten (Module) mit leichter Schattenwirkung.
- Schriftzug: "DashboardTool" in einer klaren Sans-Serif-Schrift darunter.

Dieses Logo lässt sich mit einfachen Vektorformen (z.B. Inkscape-Befehl
`Path > Object to Path`) nachbauen.

## Weiteres Vorgehen

1. Farben und Kontraste vor der Umsetzung mit dem Bericht aus
   `DashboardApp.render()['themes']` prüfen.
2. Für interaktive Prototypen ein Framework wie Figma oder Penpot nutzen.
3. Tastatur-Navigation regelmäßig testen (`CTRL+ALT+S` für die Sidebar,
   `CTRL+ALT+F` für den Fokus eines Moduls), um Barrierefreiheit sicherzustellen.
