# tests/test_ledger.py

from substrate.credits.ledger import CreditLedger


def test_ledger_append_and_chain():
    ledger = CreditLedger()

    ledger.append("echo:1.0", 3)
    ledger.append("echo:1.0", 2)

    events = ledger.events()

    assert len(events) == 2
    assert events[0].prev_hash is None
    assert events[1].prev_hash == events[0].hash
