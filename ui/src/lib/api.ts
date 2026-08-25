import { invoke } from "@tauri-apps/api/core";

export async function runWasm(input: any) {
  return await invoke("run_wasm", { input });
}
