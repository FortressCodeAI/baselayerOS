import { mkdirSync, cpSync, existsSync } from "node:fs";
import { join } from "node:path";

type ArtifactSpec = {
  id: string;
  source: string;
  target: string;
};

function getArtifacts(): ArtifactSpec[] {
  return [
    // WASM
    {
      id: "wasm-core",
      source: "dist/wasm/core.wasm",
      target: "release/wasm/core.wasm"
    },

    // Rust binaries
    {
      id: "kernel",
      source: "dist/rust/kernel",
      target: "release/rust/kernel"
    },
    {
      id: "substrate",
      source: "dist/rust/substrate",
      target: "release/rust/substrate"
    },
    {
      id: "envelopes",
      source: "dist/rust/envelopes",
      target: "release/rust/envelopes"
    },
    {
      id: "adapters",
      source: "dist/rust/adapters",
      target: "release/rust/adapters"
    },
    {
      id: "cli",
      source: "dist/rust/cli",
      target: "release/rust/cli"
    },

    // UI
    {
      id: "ui-web",
      source: "ui/dist",
      target: "release/ui/web"
    },
    {
      id: "ui-tauri",
      source: "dist/ui/tauri",
      target: "release/ui/tauri"
    },

    // Manifests
    {
      id: "build-manifest",
      source: "dist/build-manifest.json",
      target: "release/manifests/build-manifest.json"
    },
    {
      id: "determinism-manifest",
      source: "dist/determinism-manifest.json",
      target: "release/manifests/determinism-manifest.json"
    }
  ];
}

export function packageArtifacts() {
  const distRoot = join(process.cwd(), "dist");
  const releaseRoot = join(distRoot, "artifacts", "release");

  mkdirSync(releaseRoot, { recursive: true });

  const artifacts = getArtifacts();

  for (const artifact of artifacts) {
    const src = join(process.cwd(), artifact.source);
    const dst = join(releaseRoot, artifact.target);

    if (!existsSync(src)) {
      console.warn(`⚠️ Skipping missing artifact: ${artifact.id} (${artifact.source})`);
      continue;
    }

    const dstDir = dst.includes(".")
      ? join(dst, "..")
      : dst;

    mkdirSync(dstDir, { recursive: true });
    cpSync(src, dst, { recursive: true });

    console.log(`📦 Packaged ${artifact.id}: ${artifact.source} -> ${dst}`);
  }

  console.log(`\n✅ Artifacts packaged into ${releaseRoot}`);
}
