import json
from baselayeros.app.service import BaseLayerService


def test_end_to_end_execution(tmp_path):
    # Minimal deterministic UES proposal
    proposal = {
        "ues_version": "1.0.0",
        "intent": {"name": "test.intent"},
        "audit": {
            "proposal_id": "test-proposal-123",
            "created_by": "tester",
            "created_at": "2025-01-01T00:00:00Z",
            "last_modified_by": "tester",
            "last_modified_at": "2025-01-01T00:00:00Z",
        },
        "state": {"status": "DRAFT"},
        "conditions": {"pre": [], "post": []},
        "constraints": {
            "safety_level": "standard",
            "compliance_targets": [],
        },
        "scores": {"cost": 0, "risk": 0, "time": 0},
        "capabilities": [],
        "plan": {
            "phases": [
                {
                    "id": "phase1",
                    "name": "Test Phase",
                    "tasks": [
                        {
                            "id": "task1",
                            "capability": "builtin.echo",
                            "inputs": {"x": 1},
                            "outputs": {},
                            "preconditions": [],
                            "postconditions": [],
                        }
                    ],
                }
            ]
        },
    }

    # Write proposal to disk
    path = tmp_path / "proposal.json"
    path.write_text(json.dumps(proposal))

    service = BaseLayerService()

    result = service.run(
        proposal=str(path),
        actor="tester",
        actor_org="test-org",
        actor_roles=["developer"],
    )

    assert result["proposal_id"] == "test-proposal-123"
    assert result["state"] == "EXECUTED"
    assert result["success"] is True
    assert result["result"]["task1"] == {"x": 1}
