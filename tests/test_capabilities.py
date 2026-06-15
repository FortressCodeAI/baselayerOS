from baselayeros.capabilities.registry import CapabilityRegistry
from baselayeros.capabilities.loader import CapabilityLoader


def test_echo_capability():
    registry = CapabilityRegistry()
    loader = CapabilityLoader(registry)
    loader.load_all()

    echo = registry.get("builtin.echo")

    assert echo.run({"a": 1}) == {"a": 1}
    assert echo.run("hello") == "hello"
    assert echo.run(123) == 123
