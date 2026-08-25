use anyhow::Result;
use serde_json::Value;

use crate::runtime::WasmEngine;
use crate::catalog::module_catalog::build_module_catalog;


pub struct ModuleRunner {
    wasm: WasmEngine,
}

impl ModuleRunner {
    pub fn new() -> Self {
        Self {
            wasm: WasmEngine::new(),
        }
    }

    pub async fn execute(&self, module_id: &str, payload: Value) -> Result<Value> {
        println!("[runtime] module='{}' executing", module_id);

        let catalog = build_module_catalog();
        let module = catalog
            .get(module_id)
            .ok_or_else(|| anyhow::anyhow!("Unknown module '{}'", module_id))?;

        let result = if module.path.ends_with(".wasm") {
            self.wasm.execute(&module.path, payload).await?
        } else {
            serde_json::json!({
                "module": module_id,
                "status": "ok",
                "payload": payload,
            })
        };

        println!("[runtime] module='{}' completed", module_id);

        Ok(result)
    }
}
