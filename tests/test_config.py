from src.dashboardtool import DEFAULT_CONFIG


def test_has_four_theme_presets():
    assert len(DEFAULT_CONFIG.themes) == 4


def test_theme_contains_required_keys():
    required = {
        "background",
        "surface",
        "primary",
        "secondary",
        "accent",
        "text_primary",
        "text_secondary",
    }
    for name, theme in DEFAULT_CONFIG.themes.items():
        assert required.issubset(theme.keys()), f"Theme {name} fehlt Angaben"


def test_autosave_configuration():
    assert DEFAULT_CONFIG.autosave_interval_minutes == 10
    assert "timer" in DEFAULT_CONFIG.autosave_triggers
