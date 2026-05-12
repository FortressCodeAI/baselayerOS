# tests/test_burn.py

from substrate.credits.burn import burner, ledger


def test_giu_burn():
    # Reset ledger for test
    ledger._events.clear()

    receipt = burner.burn("echo", "1.0", 5)

    assert receipt["amount"] == 5
    assert receipt["total_burned"] == 5

    events = ledger.events()
    assert len(events) == 1
    assert events[0].amount == 5
