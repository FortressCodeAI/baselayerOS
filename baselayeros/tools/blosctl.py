import argparse

from baselayeros.config.config_loader import ConfigLoader
from baselayeros.config.config_validator import ConfigValidator
from baselayeros.regulus.policy_linter import PolicyLinter
from baselayeros.regulus.dashboard import RegulusDashboard
from kali.audit_chain import AuditChain


def main():
    parser = argparse.ArgumentParser(prog="blosctl")
    parser.add_argument("command", choices=["load", "validate", "lint", "dashboard"])
    parser.add_argument("--config", type=str, help="Path to config file")
    parser.add_argument("--contract", type=str, help="Path to operator_contract.json")

    args = parser.parse_args()

    if args.command == "load":
        cfg = ConfigLoader.load(args.config)
        print(cfg)

    elif args.command == "validate":
        cfg = ConfigLoader.load(args.config)
        ConfigValidator.validate(cfg)
        print("Config OK")

    elif args.command == "lint":
        linter = PolicyLinter()
        issues = linter.lint(args.contract)
        if issues:
            print("Policy Lint Issues:")
            for i in issues:
                print(f"- {i}")
        else:
            print("Policy Contract OK")

    elif args.command == "dashboard":
        audit = AuditChain()
        dash = RegulusDashboard(audit_chain=audit)
        print(dash.render_cli())


if __name__ == "__main__":
    main()
