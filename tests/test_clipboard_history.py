from rword.ui.dialogs.clipboard_history import ClipboardHistory


def test_history_starts_empty():
    assert ClipboardHistory().items == []


def test_history_adds_items_in_order():
    history = ClipboardHistory()
    history.add("uno")
    history.add("dos")
    history.add("tres")
    assert history.items == ["tres", "dos", "uno"]


def test_history_moves_existing_item_to_front():
    history = ClipboardHistory()
    history.add("uno")
    history.add("dos")
    history.add("uno")
    assert history.items == ["uno", "dos"]


def test_history_ignores_empty():
    history = ClipboardHistory()
    history.add("")
    history.add("   ")
    assert history.items == []


def test_history_limits_entries():
    history = ClipboardHistory(max_entries=3)
    for i in range(6):
        history.add(f"item{i}")
    assert history.items == ["item5", "item4", "item3"]


def test_history_clear():
    history = ClipboardHistory()
    history.add("x")
    history.clear()
    assert history.items == []
