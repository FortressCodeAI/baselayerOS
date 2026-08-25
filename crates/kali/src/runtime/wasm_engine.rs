use anyhow::Result;
use serde_json::{Value, json};
use std::fs;
use wasmtime::*;
use wasmtime_wasi::WasiCtxBuilder;


pub struct WasmEngine {
    engine: Engine,
}

impl WasmEngine {
    pub fn new() -> Self {
        let mut config = Config::new();
        config.consume_fuel(true);
        config.wasm_multi_memory(true);
        config.wasm_memory64(true);
        config.wasm_component_model(true);

        let engine = Engine::new(&config).expect("Failed to initialize Wasm engine");

        Self { engine }
    }

    pub async fn execute(&self, module_path: &str, payload: Value) -> Result<Value> {
        println!("[wasm] loading module '{}'", module_path);

        let wasm_bytes = fs::read(module_path)?;

        let module = Module::new(&self.engine, &wasm_bytes)?;

        let mut store = Store::new(&self.engine, WasiCtxBuilder::new().build());
        store.add_fuel(10_000_000)?; // deterministic fuel limit

        let instance = Instance::new(&mut store, &module, &[])?;

        let run_func = instance
            .get_typed_func::<(String,), String>(&mut store, "run")
            .map_err(|_| anyhow::anyhow!("WASM module missing required 'run' function"))?;

        let input_json = payload.to_string();

        let output_json = run_func.call(&mut store, (input_json,))?;

        let result: Value = serde_json::from_str(&output_json)?;

        println!("[wasm] module '{}' executed deterministically", module_path);

        Ok(result)
    }
}
