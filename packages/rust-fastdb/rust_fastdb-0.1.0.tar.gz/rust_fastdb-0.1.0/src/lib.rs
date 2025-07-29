mod db;
mod query;

use pyo3::prelude::*;
use query::{run_manual_query_with_params, run_query_simple, insert_data, update_data, delete_data};

/// A Python module implemented in Rust.
#[pymodule]
fn rust_fastdb(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(run_manual_query_with_params, m)?)?;
    m.add_function(wrap_pyfunction!(run_query_simple, m)?)?;
    m.add_function(wrap_pyfunction!(insert_data, m)?)?;
    m.add_function(wrap_pyfunction!(update_data, m)?)?;
    m.add_function(wrap_pyfunction!(delete_data, m)?)?;
    Ok(())
}
