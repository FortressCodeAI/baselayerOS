# baselayeros/config/config_validator.py

from typing import Dict, Any


class ConfigValidationError(Exception):
    pass


class ConfigValidator:
    """
    Validates BaseLayerOS configuration dictionaries.
    """

    REQUIRED_TOP_LEVEL = ["engine", "regulus", "company"]

    @staticmethod
    def validate(config: Dict[str, Any]) -> None:
        ConfigValidator._check_required(config)
        ConfigValidator._check_risk_tier(config)
        ConfigValidator._check_smtp(config)
        ConfigValidator._check_company(config)

    @staticmethod
    def _check_required(config: Dict[str, Any]) -> None:
        for key in ConfigValidator.REQUIRED_TOP_LEVEL:
            if key not in config:
                raise ConfigValidationError(f"Missing required section: {key}")

    @staticmethod
    def _check_risk_tier(config: Dict[str, Any]) -> None:
        tier = config["regulus"].get("max_autonomous_risk_tier")
        if not isinstance(tier, int) or tier < 0 or tier > 10:
            raise ConfigValidationError("Invalid max_autonomous_risk_tier")

    @staticmethod
    def _check_smtp(config: Dict[str, Any]) -> None:
        smtp = config.get("smtp")
        if smtp:
            if "host" not in smtp or "port" not in smtp:
                raise ConfigValidationError("SMTP config missing host/port")

    @staticmethod
    def _check_company(config: Dict[str, Any]) -> None:
        comp = config["company"]
        if "compliance" not in comp:
            raise ConfigValidationError("Missing company.compliance section")
