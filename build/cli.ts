#!/usr/bin/env node
import { buildAll } from "./orchestrator";
import { verifyDeterminism } from "./determinism";
import { packageArtifacts } from "./artifacts";

const arg = process.argv[2] ?? "all";

if (arg === "all") {
  buildAll();
} else if (arg === "verify") {
  verifyDeterminism();
} else if (arg === "package") {
  packageArtifacts();
} else {
  console.error(`Unknown build target: ${arg}`);
  process.exit(1);
}
