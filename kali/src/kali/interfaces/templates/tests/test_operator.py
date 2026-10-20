from kali.templates.operators.main_operator import main

def test_operator():
    result = main()
    assert result["status"] == "executed"
