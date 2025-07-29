/*
 *  Copyright 2025 Colliery Software
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

use pyo3::prelude::*;

#[cfg(feature = "postgres")]
mod admin;
mod context;
mod runner;
mod task;
mod value_objects;
mod workflow;

#[cfg(feature = "postgres")]
use admin::{PyDatabaseAdmin, PyTenantConfig, PyTenantCredentials};
use context::{PyContext, PyDefaultRunnerConfig};
use runner::{PyDefaultRunner, PyPipelineResult};
use task::task as task_decorator;
use value_objects::{
    PyBackoffStrategy, PyRetryCondition, PyRetryPolicy, PyRetryPolicyBuilder, PyTaskNamespace,
    PyWorkflowContext,
};
use workflow::{register_workflow_constructor, PyWorkflow, PyWorkflowBuilder};

/// A simple hello world class for testing
#[pyclass]
pub struct HelloClass {
    message: String,
}

#[pymethods]
impl HelloClass {
    #[new]
    pub fn new() -> Self {
        HelloClass {
            message: "Hello from HelloClass!".to_string(),
        }
    }

    pub fn get_message(&self) -> String {
        self.message.clone()
    }

    pub fn __repr__(&self) -> String {
        format!("HelloClass(message='{}')", self.message)
    }
}

/// A simple hello world function for testing
#[pyfunction]
fn hello_world() -> String {
    "Hello from Cloaca backend!".to_string()
}

/// Get the backend type based on compiled features
#[pyfunction]
fn get_backend() -> &'static str {
    #[cfg(feature = "postgres")]
    {
        return "postgres";
    }

    #[cfg(feature = "sqlite")]
    {
        return "sqlite";
    }

    #[cfg(not(any(feature = "postgres", feature = "sqlite")))]
    {
        "unknown"
    }
}

/// A Python module implemented in Rust.
#[pymodule]
#[cfg(feature = "postgres")]
fn cloaca_postgres(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Simple test functions
    m.add_function(wrap_pyfunction!(hello_world, m)?)?;
    m.add_function(wrap_pyfunction!(get_backend, m)?)?;

    // Test class
    m.add_class::<HelloClass>()?;

    // Context class
    m.add_class::<PyContext>()?;

    // Configuration class
    m.add_class::<PyDefaultRunnerConfig>()?;

    // Task decorator function
    m.add_function(wrap_pyfunction!(task_decorator, m)?)?;

    // Workflow classes and functions
    m.add_class::<PyWorkflowBuilder>()?;
    m.add_class::<PyWorkflow>()?;
    m.add_function(wrap_pyfunction!(register_workflow_constructor, m)?)?;

    // Runner classes
    m.add_class::<PyDefaultRunner>()?;
    m.add_class::<PyPipelineResult>()?;

    // Value objects
    m.add_class::<PyTaskNamespace>()?;
    m.add_class::<PyWorkflowContext>()?;
    m.add_class::<PyRetryPolicy>()?;
    m.add_class::<PyRetryPolicyBuilder>()?;
    m.add_class::<PyBackoffStrategy>()?;
    m.add_class::<PyRetryCondition>()?;

    // Admin classes (PostgreSQL only)
    #[cfg(feature = "postgres")]
    {
        m.add_class::<PyDatabaseAdmin>()?;
        m.add_class::<PyTenantConfig>()?;
        m.add_class::<PyTenantCredentials>()?;
    }

    // Module metadata (version automatically added by maturin from Cargo.toml)
    m.add("__backend__", "postgres")?;

    Ok(())
}

#[pymodule]
#[cfg(feature = "sqlite")]
fn cloaca_sqlite(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Simple test functions
    m.add_function(wrap_pyfunction!(hello_world, m)?)?;
    m.add_function(wrap_pyfunction!(get_backend, m)?)?;

    // Test class
    m.add_class::<HelloClass>()?;

    // Context class
    m.add_class::<PyContext>()?;

    // Configuration class
    m.add_class::<PyDefaultRunnerConfig>()?;

    // Task decorator function
    m.add_function(wrap_pyfunction!(task_decorator, m)?)?;

    // Workflow classes and functions
    m.add_class::<PyWorkflowBuilder>()?;
    m.add_class::<PyWorkflow>()?;
    m.add_function(wrap_pyfunction!(register_workflow_constructor, m)?)?;

    // Runner classes
    m.add_class::<PyDefaultRunner>()?;
    m.add_class::<PyPipelineResult>()?;

    // Value objects
    m.add_class::<PyTaskNamespace>()?;
    m.add_class::<PyWorkflowContext>()?;
    m.add_class::<PyRetryPolicy>()?;
    m.add_class::<PyRetryPolicyBuilder>()?;
    m.add_class::<PyBackoffStrategy>()?;
    m.add_class::<PyRetryCondition>()?;

    // Module metadata (version automatically added by maturin from Cargo.toml)
    m.add("__backend__", "sqlite")?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::task::task;
    use pyo3::ffi::c_str;

    #[test]
    fn test_task_registration() {
        Python::with_gil(|py| {
            println!("=== Testing task registration ===");

            // Test 1: Create a task decorator
            let task_decorator = task(
                Some("test_task".to_string()),
                None, // dependencies
                None, // retry_attempts
                None, // retry_backoff
                None, // retry_delay_ms
                None, // retry_max_delay_ms
                None, // retry_condition
                None, // retry_jitter
            )
            .unwrap();
            println!("✓ Task decorator created");

            // Test 2: Create a mock Python function
            let mock_func = py.eval(c_str!("lambda ctx: ctx"), None, None).unwrap();
            println!("✓ Mock function created");

            // Test 3: Apply the decorator (this registers the task)
            let result = task_decorator.__call__(py, mock_func.into());

            match result {
                Ok(_) => println!("✓ Task registration succeeded"),
                Err(e) => {
                    println!("✗ Task registration failed: {}", e);
                    panic!("Task registration should succeed");
                }
            }

            // Test 4: Check if task is in the registry
            let registry = cloacina::task::global_task_registry();
            let guard = registry.read().unwrap();
            let namespace =
                cloacina::TaskNamespace::new("public", "embedded", "default", "test_task");
            let constructor = guard.get(&namespace);

            assert!(constructor.is_some(), "Task should be found in registry");
            println!("✓ Task found in registry with namespace: {:?}", namespace);
        });
    }

    #[test]
    fn test_workflow_add_task_lookup() {
        Python::with_gil(|py| {
            println!("=== Testing workflow task lookup ===");

            // Test 1: Register a task first
            let task_decorator = task(
                Some("lookup_test_task".to_string()),
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            )
            .unwrap();

            let mock_func = py.eval(c_str!("lambda ctx: ctx"), None, None).unwrap();
            task_decorator.__call__(py, mock_func.into()).unwrap();
            println!("✓ Task 'lookup_test_task' registered");

            // Test 2: Create workflow builder
            let mut builder = PyWorkflowBuilder::new("lookup_test_workflow");
            println!("✓ Workflow builder 'lookup_test_workflow' created");

            // Test 3: Try to add the task (this is where it might hang)
            let task_id = py.eval(c_str!("'lookup_test_task'"), None, None).unwrap();

            println!("About to call add_task with task_id: lookup_test_task");
            println!("This is where the hang might occur...");

            let result = builder.add_task(py, task_id.into());

            match result {
                Ok(_) => println!("✓ Task added to workflow successfully"),
                Err(e) => {
                    println!("✗ Failed to add task to workflow: {}", e);
                    // Don't panic here - let's see what the error is
                }
            }
        });
    }

    #[test]
    fn test_namespace_investigation() {
        println!("=== Investigating namespace issue ===");

        // Test the namespace creation and lookup manually
        let registry = cloacina::task::global_task_registry();

        // Register a mock task with default namespace
        let default_ns =
            cloacina::TaskNamespace::new("public", "embedded", "default", "investigation_task");
        cloacina::register_task_constructor(default_ns.clone(), {
            move || {
                use std::sync::Arc;
                // Create a minimal mock task
                struct TestTask;
                #[async_trait::async_trait]
                impl cloacina::Task for TestTask {
                    async fn execute(
                        &self,
                        context: cloacina::Context<serde_json::Value>,
                    ) -> Result<cloacina::Context<serde_json::Value>, cloacina::TaskError>
                    {
                        Ok(context)
                    }
                    fn id(&self) -> &str {
                        "investigation_task"
                    }
                    fn dependencies(&self) -> &[String] {
                        &[]
                    }
                    fn retry_policy(&self) -> cloacina::retry::RetryPolicy {
                        cloacina::retry::RetryPolicy::default()
                    }
                }
                Arc::new(TestTask) as Arc<dyn cloacina::Task>
            }
        });

        // Check what namespaces exist
        {
            let guard = registry.read().unwrap();
            println!("Registry check:");

            let default_ns =
                cloacina::TaskNamespace::new("public", "embedded", "default", "investigation_task");
            let workflow_ns = cloacina::TaskNamespace::new(
                "public",
                "embedded",
                "test_workflow",
                "investigation_task",
            );

            println!("Default namespace: {:?}", default_ns);
            println!("Workflow namespace: {:?}", workflow_ns);

            println!(
                "Default namespace exists: {}",
                guard.get(&default_ns).is_some()
            );
            println!(
                "Workflow namespace exists: {}",
                guard.get(&workflow_ns).is_some()
            );
        }
    }
}
