from src.councils.router import evaluate_all

TIER_TO_LEVEL = {
    "pro": 1,
    "enterprise": 2,
    "regulated": 3,
}

def evaluate(payload):
    tier = payload.get("governance_tier", "pro")
    level = TIER_TO_LEVEL.get(tier, 1)
    return evaluate_all(level, payload)
