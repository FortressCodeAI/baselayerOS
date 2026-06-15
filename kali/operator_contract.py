import json

class OperatorContract:
    def __init__(self, contract_path="config/operator_contract.json"):
        with open(contract_path, "r") as f:
            self.contract = json.load(f)

    def should_refuse(self, node, input_payload):
        for rule in self.contract["refusal_conditions"]:
            if rule["node"] == node.name and rule["condition"](input_payload):
                return True
        return False

    def requires_human(self, node):
        return node.name in self.contract["human_required_actions"]
