# baselayeros/companies/compliance/nodes/ingest_documents.py

from dataclasses import dataclass
from kali.refusal import refuse


@dataclass
class IngestDocuments:
    """
    Deterministic document ingestion node.
    For now, returns a stub list of document identifiers.
    """

    documents: list[str] | None = None

    def run(self) -> list[str]:
        if self.documents is None:
            # Deterministic default for demo
            self.documents = ["doc_policy.pdf", "doc_procedure.pdf"]

        if not self.documents:
            refuse("No documents provided", code="NO_DOCUMENTS")

        return self.documents
