# baselayeros/companies/compliance/nodes/generate_packets.py

from dataclasses import dataclass
from kali.refusal import refuse


@dataclass
class GeneratePackets:
    """
    Deterministic compliance packet generator.
    Produces stub packet identifiers.
    """

    def run(self) -> list[str]:
        packets = [
            "packet_annual_report.zip",
            "packet_policy_review.zip",
            "packet_financial_statement.zip",
        ]

        if not packets:
            refuse("Packet generation failed", code="PACKETS_EMPTY")

        return packets
