"""Definiert Farbthemen mit hohem Kontrast und moderner Optik."""

from __future__ import annotations

from typing import Dict, Iterable, Tuple


def _hex_to_rgb(value: str) -> Tuple[float, float, float]:
    """Konvertiert HEX-Farben in RGB-Werte zwischen 0 und 1."""

    value = value.lstrip("#")
    if len(value) != 6:
        raise ValueError("Farben müssen im Format #RRGGBB vorliegen, z.B. '#112233'.")
    return tuple(int(value[i : i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[misc]


def _relative_luminance(rgb: Tuple[float, float, float]) -> float:
    """Berechnet die relative Helligkeit gemäß WCAG 2.1."""

    def transform(channel: float) -> float:
        if channel <= 0.03928:
            return channel / 12.92
        return ((channel + 0.055) / 1.055) ** 2.4

    r, g, b = map(transform, rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(color_a: str, color_b: str) -> float:
    """Berechnet den Kontrast zwischen zwei HEX-Farben."""

    lum_a = _relative_luminance(_hex_to_rgb(color_a))
    lum_b = _relative_luminance(_hex_to_rgb(color_b))
    lighter, darker = max(lum_a, lum_b), min(lum_a, lum_b)
    return (lighter + 0.05) / (darker + 0.05)


def validate_theme_accessibility(theme: Dict[str, str]) -> Dict[str, float]:
    """Prüft wichtige Kontrastverhältnisse und liefert sie zurück."""

    pairs: Iterable[Tuple[str, str]] = (
        ("text_primary", "background"),
        ("text_primary", "surface"),
        ("text_secondary", "background"),
    )
    return {
        f"{foreground}_vs_{background}": contrast_ratio(
            theme[foreground], theme[background]
        )
        for foreground, background in pairs
        if foreground in theme and background in theme
    }


THEME_PRESETS: Dict[str, Dict[str, str]] = {
    "aurora": {
        "background": "#0b132b",
        "surface": "#1c2541",
        "primary": "#5bc0be",
        "secondary": "#9fb4c7",
        "accent": "#f5a623",
        "text_primary": "#f7f9fb",
        "text_secondary": "#d2e0f2",
    },
    "sunrise": {
        "background": "#fff5f0",
        "surface": "#ffd9c2",
        "primary": "#ff7b54",
        "secondary": "#ffa26b",
        "accent": "#2b59c3",
        "text_primary": "#2a1a1f",
        "text_secondary": "#4f3d47",
    },
    "forest": {
        "background": "#0f3d3e",
        "surface": "#155e63",
        "primary": "#76c893",
        "secondary": "#f2f7f5",
        "accent": "#ffb703",
        "text_primary": "#f1faee",
        "text_secondary": "#a8dadc",
    },
    "monochrome": {
        "background": "#111111",
        "surface": "#1f1f1f",
        "primary": "#4a90e2",
        "secondary": "#50e3c2",
        "accent": "#f8e71c",
        "text_primary": "#f5f5f5",
        "text_secondary": "#cfcfcf",
    },
}
"""Vier Farbthemen mit klaren Kontrastwerten für optimale Sichtbarkeit."""
