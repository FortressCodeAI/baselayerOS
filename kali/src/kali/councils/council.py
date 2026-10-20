from kali.src.kali.councils.router import evaluate_all

TIER_TO_LEVEL = {
    "pro": 1,
    "enterprise": 2,
    "regulated": 3,
}

def evaluate(payload):
    return evaluate_all(payload)
