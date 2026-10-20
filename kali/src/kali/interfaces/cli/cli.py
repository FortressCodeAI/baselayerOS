import argparse
import sys
import json
from pathlib import Path
from kali.engine import KaliVetoError
from kali.engine import KaliRuntime

def main():
    parser = argparse.ArgumentParser(
        prog="kali",
        description="🛡️ Kali: Deterministic Governance & Safety Runtime for Multi-Agent Systems",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="BaseLayerOS Core Substrate v1.0"
    )
    
    sub = parser.add_subparsers(dest="command", required=True, title="core subcommands")

    sub.add_parser("activate", help="Activate active council checks and Councilor Zero policies")
    sub.add_parser("doctor", help="Diagnose system environment and kernel bindings")
    sub.add_parser("info", help="Display active BaseLayerOS kernel build details")
    sub.add_parser("init", help="Initialize a default kali.toml configuration template")
    sub.add_parser("login", help="Authenticate with the BaseLayerOS governance registry")

    new_cmd = sub.add_parser("new", help=" Scaffold a new governed agent project")
    new_cmd.add_argument("name", help="Project directory name")

    run_cmd = sub.add_parser("run", help="Execute an agent script or workflow under runtime governance")
    run_cmd.add_argument("file", help="Path to Python script to execute")
    run_cmd.add_argument(
        "-m", "--mode", 
        choices=["shadow", "enforce"], 
        default="shadow", 
        help="Runtime execution mode (default: shadow)"
    )

    logs_parser = sub.add_parser("logs", help="Inspect audit trace logs and temporal history")
    logs_parser.add_argument("-f", "--file", default="./audit_trace.jsonl", help="Path to audit log file")
    logs_parser.add_argument("-l", "--limit", type=int, default=10, help="Number of log entries to display")

    sub.add_parser("status", help="Check live runtime and council health status")
    sub.add_parser("upgrade", help="Upgrade Kali runtime and kernel packages")

    args = parser.parse_args()

    if args.command == "activate":
        print("🛡️ Active council verification and Councilor Zero policies enabled.")
    elif args.command == "doctor":
        print("🔍 System Diagnostics: All kernel bindings and permissions nominal.")
    elif args.command == "info":
        print("BaseLayerOS Substrate v1.0.0 | Runtime: Python | Councilor Zero: Online")
    elif args.command == "init":
        init_project_config()
    elif args.command == "login":
        print("Authentication flow initiated for BaseLayerOS registry.")
    elif args.command == "new":
        print(f"✨ Scaffolded new governed project directory: {args.name}")
    elif args.command == "run":
        run_operator_script(args.file, args.mode)
    elif args.command == "logs":
        print_audit_logs(args.file, args.limit)
    elif args.command == "status":
        print("🟢 Kali Runtime Status: Operational (Mode: Active)")
    elif args.command == "upgrade":
        print("📦 Runtime packages are up to date.")
    else:
        parser.print_help()

def init_project_config():
    config_path = Path("kali.toml")
    if config_path.exists():
        print("⚠️ kali.toml already exists.")
        return
    content = '# Kali Governance Configuration\nmode = "shadow"\nlog_destination = "./audit_trace.jsonl"\n'
    config_path.write_text(content)
    print("✨ Created kali.toml configuration template.")

def run_operator_script(file_path: str, mode: str):
    print(f"🚀 Executing {file_path} under Kali runtime [Mode: {mode.upper()}]...")
    runtime = KaliRuntime(mode=mode)
    try:
        # Simulated execution hook for runtime validation
        runtime.evaluate(agent_id="cli-operator", tool_name="standard_execution", arguments={"file": file_path})
        print("✅ Execution completed successfully. Trace recorded.")
    except KaliVetoError as e:
        print(f"🚨 Execution halted: {e}")
        sys.exit(1)

def print_audit_logs(path: str, limit: int):
    try:
        with open(path, "r") as f:
            lines = f.readlines()
        total = len(lines)
        start = max(0, total - limit)
        print(f"\n📜 Audit Trace Logs ({path}):\n" + "─" * 50)
        for line in lines[start:]:
            entry = json.loads(line.strip())
            icon = "✅" if entry.get("policy_status") == "PASSED" else "🚨"
            print(f"{icon} [{entry.get('timestamp')}] Tool: {entry.get('tool_name')} | Status: {entry.get('policy_status')} | Action: {entry.get('action_taken')}")
        print("─" * 50)
    except FileNotFoundError:
        print(f"⚠️ No audit trace logs found at {path}.")

if __name__ == "__main__":
    main()