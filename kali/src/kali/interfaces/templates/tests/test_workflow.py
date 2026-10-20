from kali.templates.operators.workflow_operator import main

def test_workflow():
    result = main()
    assert result["status"] == "workflow_completed"
