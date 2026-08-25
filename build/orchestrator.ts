import { execSync } from "node:child_process";
import { readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { generateDeterminismManifest } from "./determinism";
import { packageArtifacts } from "./artifacts";
import { generateDeterminismManifest } from "./determinism";

type Registry = {
  wasm: string[];
  rust: string[];
  ui: string[];
};

function run(cmd: string, cwd?: string) {
  console.log(`\n> ${cmd}${cwd ? ` (cwd=${cwd})` : ""}`);
  execSync(cmd, {
    stdio: "inherit",
    cwd: cwd ?? process.cwd(),
    env: process.env,
  });
}

function loadRegistry(): Registry {
  const path = join(process.cwd(), "products", "registry.json");
  const raw = readFileSync(path, "utf-8");
  return JSON.parse(raw);
}

function buildWasm(registry: Registry) {
  console.log("\n=== Building WASM modules ===");
  for (const module of registry.wasm) {
    const cratePath = join("crates", `wasm-${module}`);
    run("wasm-pack build --target web", cratePath);
  }
}

function buildRustWorkspace() {
  console.log("\n=== Building Rust workspace ===");
  run("cargo build --workspace --release");
}

function buildUI(registry: Registry) {
  console.log("\n=== Building UI (web) ===");
  run("npm install", "ui");
  run("npm run build", "ui");

  if (registry.ui.includes("tauri")) {
    console.log("\n=== Building UI (tauri) ===");
    run("npm run tauri build", "ui");
  }
}

function writeManifest() {
  console.log("\n=== Writing build manifest ===");
  const distDir = join(process.cwd(), "dist");
  mkdirSync(distDir, { recursive: true });

  const manifest = {
    built_at: new Date().toISOString(),
  };

  writeFileSync(join(distDir, "build-manifest.json"), JSON.stringify(manifest, null, 2));
}

export function buildAll() {
  const registry = loadRegistry();

  buildWasm(registry);
  buildRustWorkspace();
  buildUI(registry);
  writeManifest();
  generateDeterminismManifest();
  packageArtifacts();

  console.log("\n✅ Full build completed with artifacts packaged.");
}
