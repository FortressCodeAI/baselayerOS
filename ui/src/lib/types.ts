export type ExecutionStatus = "ok" | "error";

export interface ExecutionContext {
  tenant_id: string;
  actor_id: string;
  trace_id: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

export interface ExecutionInput {
  module_id: string;
  version: string;
  envelope_id: string;
  payload: unknown;
  context: ExecutionContext;
}

export interface InvariantResult {
  id: string;
  passed: boolean;
  message?: string;
}

export interface AuditEntry {
  id: string;
  timestamp: string;
  module_id: string;
  envelope_id: string;
  status: ExecutionStatus;
  invariants: InvariantResult[];
  metadata?: Record<string, unknown>;
}

export interface ExecutionOutput {
  module_id: string;
  version: string;
  envelope_id: string;
  status: ExecutionStatus;
  result?: unknown;
  error?: string;
  invariants: InvariantResult[];
  audit_chain: AuditEntry[];
}
