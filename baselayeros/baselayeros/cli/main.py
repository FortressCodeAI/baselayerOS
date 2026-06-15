from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from baselayeros.app.service import BaseLayerService


def main():
    parser = argparse.ArgumentParser(
        description="BaseLayerOS deterministic execution engine"
    )

    parser.add_argument(
        "proposal",
        type=str,
        help="Path to UES proposal JSON file",
    )

    parser.add_argument(
        "--actor",
        type=str,
        default="cli-user",
        help="Actor ID initiating the run",
    )

    parser.add_argument(
        "--org",
        type=str,
        default="local",
        help="Organization of the actor",
    )

    parser.add_argument(
        "--roles",
        type=str,
        nargs="*",
        default=["developer"],
        help="Actor roles",
    )

    args = parser.parse_args()

    # Validate proposal path
    path = Path(args.proposal)
    if not path.exists():
        print(f"Error: proposal file not found: {path}", file=sys.stderr)
        sys.exit(1)

    # Load proposal JSON
    try:
        with path.open("r", encoding="utf-8") as f:
            proposal_data = json.load(f)
    except Exception as e:
        print(f"Error reading proposal: {e}", file=sys.stderr)
        sys.exit(1)

    # Run through BaseLayerOS
    service = BaseLayerService()
    result = service.run(
        proposal=proposal_data,
        actor=args.actor,
        actor_org=args.org,
        actor_roles=args.roles,
    )

    # Print deterministic JSON output
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
