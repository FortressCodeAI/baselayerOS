import subprocess
import time
import socket
from pathlib import Path
from typing import List, Tuple, Optional

import click

from baselayeros.runtime.loader import load_all_modules, load_all_packs
from baselayeros.runtime.demo import init_demo_environment
from baselayeros.runtime.utils import reset_environment, print_status


# ------------------------------------------------------------
# Low-level helpers
# ------------------------------------------------------------

def _is_port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


def _wait_for_port(host: str, port: int, timeout_seconds: float = 10.0) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if _is_port_open(host, port):
            return True
        time.sleep(0.2)
    return False


def _find_available_port(preferred: int, max_tries: int = 10) -> Tuple[int, bool]:
    """
    Try preferred port; if taken, increment until a free one is found.
    Returns (port, changed_flag).
    """
    port = preferred
    for _ in range(max_tries):
        if not _is_port_open("localhost", port):
            return port, (port != preferred)
        port += 1
    # Fallback: just return preferred and let it fail
    return preferred, False


def _start_substrate_process(port: int) -> subprocess.Popen:
    server_cmd: List[str] = [
        "python",
        "-m",
        "baselayeros.runtime.server",
        "--port",
        str(port),
    ]
    return subprocess.Popen(
        server_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _read_stderr(proc: subprocess.Popen) -> Optional[str]:
    if proc.stderr:
        try:
            return proc.stderr.read().decode("utf-8", errors="ignore")
        except Exception:
            return None
    return None


# ------------------------------------------------------------
# CLI command
# ------------------------------------------------------------

@click.command(help="Start the BaseLayerOS substrate and load all governed components.")
@click.option(
    "--demo",
    is_flag=True,
    help="Start in demo mode (seed GIUs, demo identity, demo modules/packs).",
)
@click.option(
    "--reset",
    is_flag=True,
    help="Reset ledger, audit logs, and temp modules/packs before starting.",
)
@click.option(
    "--port",
    default=8000,
    show_default=True,
    help="Preferred port to run the substrate HTTP server on.",
)
@click.option(
    "--max-restarts",
    default=3,
    show_default=True,
    help="Maximum times to auto-restart substrate if it crashes on startup.",
)
def start(demo: bool, reset: bool, port: int, max_restarts: int) -> None:
    """
    Deterministic, governed bootstrap for BaseLayerOS.

    Stages:
      1. Optional reset
      2. Environment init
      3. Port selection
      4. Start substrate server (with auto-restart)
      5. Governance + module load
      6. Pack load
      7. Optional demo init
      8. Governed status report
    """

    # --------------------------------------------------------
    # 1. Optional reset
    # --------------------------------------------------------
    if reset:
        click.secho("↻ Resetting BaseLayerOS environment...", fg="yellow")
        reset_environment()
        click.secho("✓ Environment reset", fg="green")

    # Ensure .baselayeros exists
    root = Path(".baselayeros")
    root.mkdir(exist_ok=True)

    # --------------------------------------------------------
    # 2. Port selection (automatic if taken)
    # --------------------------------------------------------
    chosen_port, changed = _find_available_port(port)
    if changed:
        click.secho(
            f"⚠ Port {port} is in use, selecting {chosen_port} instead.",
            fg="yellow",
        )
    else:
        click.secho(f"Using port {chosen_port}", fg="cyan")

    # --------------------------------------------------------
    # 3. Start substrate server (with auto-restart)
    # --------------------------------------------------------
    attempts = 0
    server_proc: Optional[subprocess.Popen] = None

    while attempts <= max_restarts:
        attempts += 1
        click.secho(
            f"🚀 Starting BaseLayerOS substrate on port {chosen_port} (attempt {attempts})...",
            fg="cyan",
        )

        server_proc = _start_substrate_process(chosen_port)

        if not _wait_for_port("localhost", chosen_port, timeout_seconds=10.0):
            click.secho("❌ Substrate failed to open port in time.", fg="red")
            stderr = _read_stderr(server_proc)
            if stderr:
                click.secho("\nSubstrate stderr:", fg="red")
                click.echo(stderr)

            server_proc.terminate()
            if attempts > max_restarts:
                click.secho(
                    "❌ Max restart attempts reached. Aborting governed startup.",
                    fg="red",
                )
                return
            else:
                click.secho("↻ Retrying substrate startup...", fg="yellow")
                continue

        # Port is open; check if process is still alive
        time.sleep(0.5)
        if server_proc.poll() is not None:
            click.secho("❌ Substrate process exited shortly after start.", fg="red")
            stderr = _read_stderr(server_proc)
            if stderr:
                click.secho("\nSubstrate stderr:", fg="red")
                click.echo(stderr)

            if attempts > max_restarts:
                click.secho(
                    "❌ Max restart attempts reached. Aborting governed startup.",
                    fg="red",
                )
                return
            else:
                click.secho("↻ Retrying substrate startup...", fg="yellow")
                continue

        # Success
        break

    click.secho(f"✓ Substrate running at http://localhost:{chosen_port}", fg="green")

    # --------------------------------------------------------
    # 4. Load modules (governed components)
    # --------------------------------------------------------
    click.secho("📦 Loading modules...", fg="cyan")
    try:
        loaded_modules = load_all_modules()
    except Exception as e:
        click.secho("❌ Failed to load modules (governed failure).", fg="red")
        click.echo(repr(e))
        if server_proc:
            server_proc.terminate()
        return
    click.secho(f"✓ Loaded {len(loaded_modules)} modules", fg="green")

    # --------------------------------------------------------
    # 5. Load packs (governance / automated / compliance)
    # --------------------------------------------------------
    click.secho("📦 Loading packs...", fg="cyan")
    try:
        loaded_packs = load_all_packs()
    except Exception as e:
        click.secho("❌ Failed to load packs (governed failure).", fg="red")
        click.echo(repr(e))
        if server_proc:
            server_proc.terminate()
        return
    click.secho(f"✓ Loaded {len(loaded_packs)} packs", fg="green")

    # --------------------------------------------------------
    # 6. Optional demo initialization
    # --------------------------------------------------------
    if demo:
        click.secho(
            "🎛  Initializing demo environment (GIUs, identity, demo modules)...",
            fg="cyan",
        )
        try:
            init_demo_environment()
        except Exception as e:
            click.secho("❌ Failed to initialize demo environment.", fg="red")
            click.echo(repr(e))
            if server_proc:
                server_proc.terminate()
            return
        click.secho("✓ Demo environment initialized", fg="green")

    # --------------------------------------------------------
    # 7. Governed status report
    # --------------------------------------------------------
    print_status(
        port=chosen_port,
        modules=loaded_modules,
        packs=loaded_packs,
        demo=demo,
    )

    click.secho("\nBaseLayerOS is ready.", fg="green")
    click.echo("You can now run actions, for example:")
    click.echo(
        f"  baselayeros run credit_risk.evaluate --payload '{{\"score\": 720}}' --port {chosen_port}"
    )
    click.echo("Or inspect GIUs:")
    click.echo("  baselayeros giu balance demo-user")
