# baselayeros/companies/compliance/nodes/check_payment.py

from dataclasses import dataclass
from kali.refusal import refuse


@dataclass
class CheckPayment:
    """
    Deterministic payment verification node.
    Replace with real payment logic later.
    """

    paid: bool = True  # default for demo

    def run(self) -> str:
        if not self.paid:
            refuse("Payment not received", code="PAYMENT_REQUIRED")

        return "Payment verified"
