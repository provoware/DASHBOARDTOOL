"""Definiert Farbthemen mit hohem Kontrast und moderner Optik."""

from __future__ import annotations

from typing import Dict


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
