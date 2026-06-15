"""
demo_compliance_run.py
Minimal deterministic compliance demo using BaseLayerOS.
"""

from kali.refusal import Refusal  # noqa: F401
from kali.commit import commit_state  # noqa: F401
from kali.audit_chain import AuditChain
from kali.authority_gate import AuthorityGate

from giu.metering import Meter

from baselayeros.core.runtime.engine import ExecutionEngine

from companies.compliance.nodes.check_payment import CheckPayment
from companies.compliance.nodes.ingest_documents import IngestDocuments
from companies.compliance.nodes.extract_requirements import ExtractRequirements
from companies.compliance.nodes.generate_calendar import GenerateCalendar
from companies.compliance.nodes.generate_packets import GeneratePackets
from companies.compliance.nodes.store_audit_event import StoreAuditEvent
from companies.compliance.nodes.notify_customer import NotifyCustomer


def main() -> None:
    print("\n=== BaseLayerOS Compliance Demo ===\n")

    # Governance primitives
    audit_chain = AuditChain()
    authority = AuthorityGate()
    meter = Meter()

    # Deterministic execution engine
    engine = ExecutionEngine(
        audit_chain=audit_chain,
        authority=authority,
    )

    # Example actor + operation
    actor = "compliance_bot"
    operation = "run_compliance_pipeline"

    # Example pipeline function
    def run_pipeline():
        meter.increment()

        # Run nodes in a simple deterministic sequence
        payment = CheckPayment().run()
        docs = IngestDocuments().run()
        reqs = ExtractRequirements().run()
        cal = GenerateCalendar().run()
        packets = GeneratePackets().run()
        audit = StoreAuditEvent().run()
        notify = NotifyCustomer(demo_mode=True).run()

        return {
            "payment": payment,
            "documents": docs,
            "requirements": reqs,
            "calendar": cal,
            "packets": packets,
            "audit": audit,
            "notify": notify,
            "meter_count": meter.count,
        }

    # Execute under governance
    result = engine.run(
        actor=actor,
        operation=operation,
        fn=run_pipeline,
    )

    # Output
    if result.success:
        print("Pipeline completed successfully.\n")
        print("Committed State:")
        print(result.value)
    else:
        print("Pipeline failed.")
        print("Error:", result.error)

    print("\nAudit Events:")
    for event in audit_chain.events:
        print(f"- {event.event_type.upper()}: {event.detail}")


if __name__ == "__main__":
    main()
