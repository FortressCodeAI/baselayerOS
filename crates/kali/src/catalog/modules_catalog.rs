use std::collections::HashMap;

use crate::registry::ModuleSpec;

pub fn build_module_catalog() -> HashMap<String, ModuleSpec> {
    let mut modules = HashMap::new();

    modules.insert(
        "core_module".into(),
        ModuleSpec {
            id: "core_module".into(),
            description: "Core deterministic module".into(),
            version: "1.0.0".into(),
            path: "modules/core/core.wasm".into(),
        },
    );

    modules.insert(
        "marketing_module".into(),
        ModuleSpec {
            id: "marketing_module".into(),
            description: "Deterministic marketing module".into(),
            version: "1.0.0".into(),
            path: "modules/marketing/marketing.wasm".into(),
        },
    );

    modules.insert(
        "sales_module".into(),
        ModuleSpec {
            id: "sales_module".into(),
            description: "Deterministic sales module".into(),
            version: "1.0.0".into(),
            path: "modules/sales/sales.wasm".into(),
        },
    );

    modules
}
