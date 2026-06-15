# baselayeros/kali/human_callback.py

"""
Simple, production-ready human callback for AuthorityGate.

You can:
- hardcode decisions for testing
- load decisions from a queue
- load decisions from a UI
- load decisions from a database
- load decisions from a CLI prompt
"""

def human_callback(node, action: str):
    """
    Return a tuple: (decision, reason)

    decision must be:
        "approve" or "deny"

    reason is a human-readable explanation.
    """

    # --- OPTION 1: Always approve (default for automated runs) ---
    return ("approve", f"Approved execution of {node.name}")

    # --- OPTION 2: Always deny ---
    # return ("deny", f"Denied execution of {node.name}")

    # --- OPTION 3: Interactive CLI prompt ---
    # print(f"\nAuthority Gate Triggered for node: {node.name}")
    # print(f"Action: {action}")
    # choice = input("Approve? (y/n): ").strip().lower()
    # if choice == "y":
    #     return ("approve", "Approved by human operator")
    # return ("deny", "Denied by human operator")

    # --- OPTION 4: Load from a queue or DB ---
    # decision_record = load_decision_from_db(node.name)
    # return (decision_record["decision"], decision_record["reason"])
