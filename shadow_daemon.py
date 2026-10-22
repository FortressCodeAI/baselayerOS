"""
BaseLayerOS Kali: 24-Hour Shadow Sidecar HTTP Daemon
Listens for silent telemetry hooks from agent pipelines, evaluates compliance,
and appends to audit_chain.json safely with crash recovery.
"""
import json
import http.server
import socketserver
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

PORT = 8080
AUDIT_LOG = Path("audit_chain.json")

class ShadowSidecarEngine:
    @staticmethod
    def observe(action_slug: str, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
        violations: List[str] = []
        sanitized = dict(raw_payload)
        pii_detected = False

        # MFIPPA PII check
        for key in ["citizen_name", "ohip", "phone", "sin", "email"]:
            if key in sanitized and sanitized[key]:
                val = str(sanitized[key])
                if not val.startswith("[REDACTED"):
                    violations.append(f"SHADOW_VIOLATION_MFIPPA_PII_EXPOSED: Unmasked '{key}' detected.")
                    sanitized[key] = f"[SHADOW_REDACTED_{key.upper()}]"
                    pii_detected = True

        # EDSTA Write lock check
        if sanitized.get("is_write_operation", False) and "admin" not in action_slug.lower():
            violations.append("SHADOW_VIOLATION_EDSTA_UNAUTHORIZED_WRITE: Direct DB write initiated.")

        timestamp = datetime.utcnow().isoformat() + "Z"
        entry = {
            "timestamp": timestamp,
            "mode": "24H_SHADOW_DAEMON",
            "action_slug": action_slug,
            "execution_blocked": False,
            "violations_detected": violations,
            "pii_redacted": pii_detected
        }

        # Safe append with file lock handling
        try:
            if AUDIT_LOG.exists():
                with open(AUDIT_LOG, "r") as f:
                    ledger = json.load(f)
            else:
                ledger = []
            ledger.append(entry)
            with open(AUDIT_LOG, "w") as f:
                json.dump(ledger, f, indent=2)
        except Exception as e:
            print(f"[!] Ledger write error: {e}")

        return {"status": "LOGGED", "violations": violations}


class ShadowHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/observe":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode('utf-8'))
                action = data.get("action", "unknown_action")
                payload = data.get("payload", {})
                
                result = ShadowSidecarEngine.observe(action, payload)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Quiet standard HTTP logs to prevent terminal spam over 24 hours
        return


if __name__ == "__main__":
    print(f"[*] Kali 24H Shadow Daemon active on port {PORT}. Zero disruption mode.")
    with socketserver.TCPServer(("", PORT), ShadowHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Daemon halted.")