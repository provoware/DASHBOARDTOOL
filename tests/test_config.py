from src.dashboardtool import DEFAULT_CONFIG, validate_theme_accessibility


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


def test_breakpoint_for_width_changes_with_size():
    mobile = DEFAULT_CONFIG.breakpoint_for_width(480)
    desktop = DEFAULT_CONFIG.breakpoint_for_width(1400)

    assert mobile["name"] == "mobile"
    assert desktop["name"] in {"desktop", "wide"}
    assert desktop["columns"] >= mobile["columns"]


def test_theme_accessibility_is_above_minimum():
    for theme in DEFAULT_CONFIG.themes.values():
        report = validate_theme_accessibility(theme)
        assert report, "Es sollten Kontrastwerte berechnet werden"
        assert all(value >= 4.5 for value in report.values())
