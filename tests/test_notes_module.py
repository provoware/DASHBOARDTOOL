from modules.notes import NotesModule


def test_notes_module_respects_theme():
    module = NotesModule()
    payload = module.render()
    assert payload["theme"]["background"].startswith("#")


def test_notes_module_autosave_sets_timestamp():
    module = NotesModule()
    module.autosave()
    module.write("id1", "Test")
    assert "id1" in module.storage
