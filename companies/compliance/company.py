"""
ComplianceCompany: a deterministic automated company wrapper
around the compliance graph.
"""

from dataclasses import dataclass
from typing import Any, Dict

from kali.audit_chain import AuditChain
from kali.authority_gate import AuthorityGate
from baselayeros.core.runtime.engine import ExecutionEngine
from companies.compliance.graph import ComplianceGraph


@dataclass
class ComplianceCompany:
    """
    A minimal automated company that runs the compliance graph
    under governance.
    """

    audit_chain: AuditChain
    authority: AuthorityGate
    engine: ExecutionEngine
    graph: ComplianceGraph

    @classmethod
    def bootstrap(cls) -> "ComplianceCompany":
        audit_chain = AuditChain()
        authority = AuthorityGate()
        engine = ExecutionEngine(audit_chain=audit_chain, authority=authority)
        graph = ComplianceGraph(engine=engine)
        return cls(
            audit_chain=audit_chain,
            authority=authority,
            engine=engine,
            graph=graph,
        )

    def run_once(self, actor: str = "compliance_bot") -> Dict[str, Any]:
        """
        Run the compliance graph once under governance.
        """
        return self.graph.run(actor=actor)

    def get_audit_events(self) -> list:
        return self.audit_chain.events
