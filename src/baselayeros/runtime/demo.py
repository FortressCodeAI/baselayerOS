from baselayeros.credits.billing import Billing


def init_demo_environment():
    """
    Seed a demo identity + GIUs and ensure at least one demo module is present.
    """
    billing = Billing()

    demo_account = "demo-user"
    # Seed 100 GIUs for demo
    billing.credit(demo_account, 100, meta={"reason": "demo_seed"})

    # You can also ensure demo modules are imported here if needed
    # e.g., import baselayeros.modules.demo_credit_risk  # noqa: F401
