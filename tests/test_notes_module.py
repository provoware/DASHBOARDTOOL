import pytest

from modules.notes import NotesModule


def test_notes_module_respects_theme():
    module = NotesModule()
    payload = module.render()
    assert payload["theme"]["background"].startswith("#")
    assert payload["breakpoints"], "Breakpoints sollten vorhanden sein"
    assert "focus" in payload["keyboard_shortcuts"]
    assert "timer" in payload["autosave_triggers"]
    assert payload["storage_directory"].endswith("notes")


def test_notes_module_autosave_sets_timestamp():
    module = NotesModule()
    module.autosave()
    module.write("id1", "Test")
    assert "id1" in module.storage


def test_notes_module_lists_and_reads_notes():
    module = NotesModule()
    module.write("id1", "Inhalt")
    assert module.read("id1")["content"] == "Inhalt"
    assert module.list_note_ids() == ["id1"]


def test_notes_module_rejects_empty_id():
    module = NotesModule()
    with pytest.raises(ValueError):
        module.write("", "Inhalt")
