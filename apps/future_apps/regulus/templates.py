def compliance_company_mvp_template():
    return {
        "name": "ComplianceCompanyMVP",
        "nodes": [
            {"name": "CheckPaymentStatus", "handler": None, "contract_clause": "payments"},
            {"name": "IngestDocuments", "handler": None, "contract_clause": "documents"},
            {"name": "ExtractRequirements", "handler": None, "contract_clause": "requirements"},
            {"name": "GenerateCalendar", "handler": None, "contract_clause": "calendar"},
            {"name": "GeneratePackets", "handler": None, "contract_clause": "packets"},
            {"name": "StoreAuditEvent", "handler": None, "contract_clause": "audit"},
            {"name": "NotifyCustomer", "handler": None, "contract_clause": "notifications"}
        ],
        "edges": [
            {"from": "CheckPaymentStatus", "to": "IngestDocuments"},
            {"from": "IngestDocuments", "to": "ExtractRequirements"},
            {"from": "ExtractRequirements", "to": "GenerateCalendar"},
            {"from": "GenerateCalendar", "to": "GeneratePackets"},
            {"from": "GeneratePackets", "to": "StoreAuditEvent"},
            {"from": "StoreAuditEvent", "to": "NotifyCustomer"}
        ],
        "entrypoint": "CheckPaymentStatus"
    }
