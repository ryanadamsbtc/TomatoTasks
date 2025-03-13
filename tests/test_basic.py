from tomatotasks import storage


def test_add_and_list_roundtrip(tmp_path, monkeypatch):
    # Force storage path into tmp directory
    home = tmp_path
    monkeypatch.setenv("HOME", str(home))
    t = storage.add_task("demo")
    items = storage.list_tasks()
    assert any(i.id == t.id for i in items)

