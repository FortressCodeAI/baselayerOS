import json
from jsonschema import Draft202012Validator

from schemas.ues.v1_0_0.ues_types import UES


class UESValidationError(Exception):
    pass


class UESValidator:
    def __init__(self, schema_path: str):
        with open(schema_path, "r") as f:
            self.schema = json.load(f)
        self.validator = Draft202012Validator(self.schema)

    def validate(self, proposal: dict) -> UES:
        errors = sorted(self.validator.iter_errors(proposal), key=lambda e: e.path)
        if errors:
            messages = [f"{'/'.join(map(str, e.path))}: {e.message}" for e in errors]
            raise UESValidationError("\n".join(messages))

        # Convert dict → typed UES dataclass
        return UES(**proposal)
