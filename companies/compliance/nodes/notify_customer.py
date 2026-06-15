# baselayeros/companies/compliance/nodes/notify_customer.py

from dataclasses import dataclass
from companies.compliance.integrations.email.smtpd import SMTPClient, SMTPConfig
from kali.refusal import refuse


@dataclass
class NotifyCustomer:
    customer_email: str = "customer@example.com"
    demo_mode: bool = True  # <— key addition

    def run(self) -> str:
        if not self.customer_email:
            refuse("No customer email provided", code="NO_EMAIL")

        if self.demo_mode:
            config = SMTPConfig(
                host="localhost",
                port=1025,
                use_tls=False,
            )
        else:
            config = SMTPConfig(
                host="smtp.example.com",
                port=587,
                username="noreply@example.com",
                password="password123",
                use_tls=True,
            )

        client = SMTPClient(config)

        subject = "Your Compliance Package Is Ready"
        body = (
            "Hello,\n\n"
            "Your compliance documents have been processed successfully.\n"
            "You may now review your updated compliance calendar and packets.\n\n"
            "Regards,\nCompliance Automation Bot"
        )

        client.send(
            to=self.customer_email,
            subject=subject,
            body=body,
        )

        return f"Notification sent to {self.customer_email}"
