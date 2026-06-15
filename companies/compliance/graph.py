"""
Compliance graph: deterministic DAG over compliance nodes,
executed via the shared GraphExecutor + ExecutionEngine.
"""

from dataclasses import dataclass

from baselayeros.actiongraph.executor import GraphExecutor, Node
from baselayeros.core.runtime.engine import ExecutionEngine
from kali.audit_chain import AuditChain
from kali.authority_gate import AuthorityGate

from companies.compliance.nodes.check_payment import CheckPayment
from companies.compliance.nodes.ingest_documents import IngestDocuments
from companies.compliance.nodes.extract_requirements import ExtractRequirements
from companies.compliance.nodes.generate_calendar import GenerateCalendar
from companies.compliance.nodes.generate_packets import GeneratePackets
from companies.compliance.nodes.store_audit_event import StoreAuditEvent
from companies.compliance.nodes.notify_customer import NotifyCustomer


@dataclass
class ComplianceGraph:
    engine: ExecutionEngine

    def build_executor(self) -> GraphExecutor:
        gx = GraphExecutor(engine=self.engine)

        # Nodes
        gx.add_node(Node("check_payment", CheckPayment().run))
        gx.add_node(Node("ingest_documents", IngestDocuments().run))
        gx.add_node(Node("extract_requirements", ExtractRequirements().run))
        gx.add_node(Node("generate_calendar", GenerateCalendar().run))
        gx.add_node(Node("generate_packets", GeneratePackets().run))
        gx.add_node(Node("store_audit_event", StoreAuditEvent().run))
        gx.add_node(Node("notify_customer", NotifyCustomer().run))

        # Edges (dependencies)
        gx.add_edge("check_payment", "ingest_documents")
        gx.add_edge("ingest_documents", "extract_requirements")
        gx.add_edge("extract_requirements", "generate_calendar")
        gx.add_edge("generate_calendar", "generate_packets")
        gx.add_edge("generate_packets", "store_audit_event")
        gx.add_edge("store_audit_event", "notify_customer")

        return gx

    def run(self, actor: str = "compliance_bot") -> dict:
        gx = self.build_executor()
        return gx.execute(actor=actor, operation_prefix="compliance")
