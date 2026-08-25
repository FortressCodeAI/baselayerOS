import { createHash } from "node:crypto";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

type Artifact = {
  id: string;
  path: string;
};

type DeterminismManifest = {
  version: number;
  generated_at: string;
  artifacts: {
    id: string;
    path: string;
    sha256: string;
  }[];
};

function hashFile(path: string): string {
  const data = readFileSync(path);
  const hash = createHash("sha256");
  hash.update(data);
  return hash.digest("hex");
}

function loadArtifacts(): Artifact[] {
  // You can make this dynamic later; for now we hard‑code based on registry.json
  return [
    { id: "wasm-core", path: "dist/wasm/core.wasm" },
    { id: "kernel", path: "dist/rust/kernel" },
    { id: "substrate", path: "dist/rust/substrate" },
    { id: "envelopes", path: "dist/rust/envelopes" },
    { id: "adapters", path: "dist/rust/adapters" },
    { id: "cli", path: "dist/rust/cli" },
    { id: "ui-web", path: "ui/dist/index.html" },
    { id: "ui-tauri", path: "dist/ui/tauri" }
  ];
}

export function generateDeterminismManifest() {
  const artifacts = loadArtifacts();
  const distDir = join(process.cwd(), "dist");
  mkdirSync(distDir, { recursive: true });

  const manifest: DeterminismManifest = {
    version: 1,
    generated_at: new Date().toISOString(),
    artifacts: []
  };

  for (const artifact of artifacts) {
    const fullPath = join(process.cwd(), artifact.path);
    if (!existsSync(fullPath)) {
      console.warn(`⚠️ Artifact missing: ${artifact.id} (${artifact.path})`);
      continue;
    }

    const sha256 = hashFile(fullPath);
    manifest.artifacts.push({
      id: artifact.id,
      path: artifact.path,
      sha256
    });
  }

  const manifestPath = join(distDir, "determinism-manifest.json");
  writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
  console.log(`✅ Determinism manifest written to ${manifestPath}`);
}

export function verifyDeterminism() {
  const distDir = join(process.cwd(), "dist");
  const manifestPath = join(distDir, "determinism-manifest.json");

  if (!existsSync(manifestPath)) {
    console.error("❌ No determinism manifest found. Run generateDeterminismManifest first.");
    process.exit(1);
  }

  const raw = readFileSync(manifestPath, "utf-8");
  const manifest: DeterminismManifest = JSON.parse(raw);

  let allMatch = true;

  for (const artifact of manifest.artifacts) {
    const fullPath = join(process.cwd(), artifact.path);
    if (!existsSync(fullPath)) {
      console.error(`❌ Missing artifact: ${artifact.id} (${artifact.path})`);
      allMatch = false;
      continue;
    }

    const currentHash = hashFile(fullPath);
    if (currentHash !== artifact.sha256) {
      console.error(
        `❌ Hash mismatch for ${artifact.id}: expected ${artifact.sha256}, got ${currentHash}`
      );
      allMatch = false;
    } else {
      console.log(`✅ ${artifact.id} is deterministic (sha256=${currentHash})`);
    }
  }

  if (!allMatch) {
    console.error("❌ Determinism verification FAILED.");
    process.exit(1);
  }

  console.log("✅ Determinism verification PASSED.");
}
