from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Customer:
    id: str
    name: str
    email: str
    tier: str

@dataclass
class Document:
    id: str
    customer_id: str
    type: str
    path: str

@dataclass
class Requirement:
    id: str
    customer_id: str
    description: str
    due_date: str

@dataclass
class Packet:
    id: str
    customer_id: str
    requirements: List[str]
    generated_at: str
