use pyo3::prelude::*;
use serde_json::{json, Value as JsonValue};
use sqlx::{Column, Row};
use crate::db::get_or_create_pool;
use std::collections::HashMap;
use pyo3::types::{PyDict, PyList};
use pyo3_asyncio::TaskLocals;
use sqlx::TypeInfo;
// Helper function to convert SQLx errors to PyErr
fn sqlx_err_to_py(err: sqlx::Error) -> PyErr {
    PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(err.to_string())
}

// Add helper to determine database type
fn get_db_type(url: &str) -> Result<&'static str, PyErr> {
    if url.starts_with("postgres://") || url.starts_with("postgresql://") {
        Ok("postgres")
    } else if url.starts_with("mysql://") {
        Ok("mysql")
    } else if url.starts_with("sqlite:") {
        Ok("sqlite")
    } else {
        Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "Unsupported database URL scheme",
        ))
    }
}

#[pyfunction]
pub fn run_manual_query_with_params(
    py: Python<'_>,
    db_url: String,
    query: String,
    params: &PyList,
    use_cache: bool,
) -> PyResult<PyObject> {
    // Validate database type
    get_db_type(&db_url)?;

    // Important: Register available drivers to sqlx::any
    sqlx::any::install_default_drivers();
    
    let params: Vec<JsonValue> = params.iter().map(|item| {
        if item.is_none() {
            Ok(JsonValue::Null)
        } else if let Ok(s) = item.extract::<String>() {
            Ok(JsonValue::String(s))
        } else if let Ok(i) = item.extract::<i64>() {
            Ok(JsonValue::Number(i.into()))
        } else if let Ok(f) = item.extract::<f64>() {
            Ok(JsonValue::Number(json!(f).as_number().unwrap().clone()))
        } else {
            Ok(JsonValue::Null)
        }
    }).collect::<PyResult<_>>()?;

    let locals = TaskLocals::with_running_loop(py)?;
    let fut = async move {
        let pool = get_or_create_pool(&db_url, use_cache).await.map_err(sqlx_err_to_py)?;
        let mut query_builder = sqlx::query(&query);
        
        for param in &params {
            match param {
                JsonValue::Null => query_builder = query_builder.bind(None::<String>),
                JsonValue::Bool(b) => query_builder = query_builder.bind(*b),
                JsonValue::Number(n) => {
                    if let Some(i) = n.as_i64() {
                        query_builder = query_builder.bind(i);
                    } else if let Some(f) = n.as_f64() {
                        query_builder = query_builder.bind(f);
                    }
                },
                JsonValue::String(s) => query_builder = query_builder.bind(s),
                _ => {}
            }
        }
        
        let rows = query_builder.fetch_all(&pool).await.map_err(sqlx_err_to_py)?;
        let results = rows.into_iter().map(|row| {
            let mut map = serde_json::Map::new();
            for column in row.columns() {
                let name = column.name();
                let db_type = column.type_info().name().to_uppercase();
                
                // Optional: Debug log
                // println!("Column '{}' has DB type '{}'", name, db_type);
        
                let value: JsonValue = if db_type.contains("CHAR") || db_type.contains("TEXT") || db_type.contains("STRING") {
                    row.try_get::<Option<String>, _>(name).ok().flatten().map_or_else(
                        || JsonValue::Null,
                        |v| json!(v)
                    )
                } else if db_type.contains("INT") || db_type.contains("BIGINT") || db_type.contains("SMALLINT") {
                    row.try_get::<Option<i64>, _>(name).ok().flatten().map_or_else(
                        || JsonValue::Null,
                        |v| json!(v)
                    )
                } else if db_type.contains("FLOAT") || db_type.contains("REAL") || db_type.contains("DOUBLE") || db_type.contains("NUMERIC") {
                    row.try_get::<Option<f64>, _>(name).ok().flatten().map_or_else(
                        || JsonValue::Null,
                        |v| json!(v)
                    )
                } else if db_type.contains("BOOL") {
                    row.try_get::<Option<bool>, _>(name).ok().flatten().map_or_else(
                        || JsonValue::Null,
                        |v| json!(v)
                    )
                } else {
                    // Fallback: try as string first before null
                    row.try_get::<Option<String>, _>(name).ok().flatten().map_or(JsonValue::Null, |v| json!(v))
                };
        
                map.insert(name.to_string(), value);
            }
            JsonValue::Object(map)
        }).collect::<Vec<_>>();
        
        Python::with_gil(|py| {
            let py_list = PyList::empty(py);
            for result in results {
                let py_dict = PyDict::new(py);
                if let JsonValue::Object(map) = result {
                    for (k, v) in map {
                        let py_value = match v {
                            JsonValue::Null => py.None(),
                            JsonValue::Bool(b) => b.into_py(py),
                            JsonValue::Number(n) => {
                                if let Some(i) = n.as_i64() {
                                    i.into_py(py)
                                } else if let Some(f) = n.as_f64() {
                                    f.into_py(py)
                                } else {
                                    py.None()
                                }
                            },
                            JsonValue::String(s) => s.into_py(py),
                            _ => py.None()
                        };
                        py_dict.set_item(k, py_value)?;
                    }
                }
                py_list.append(py_dict)?;
            }
            Ok::<Py<PyAny>, PyErr>(py_list.into_py(py))
        })
    };

    pyo3_asyncio::tokio::future_into_py_with_locals::<_, Py<PyAny>>(py, locals, fut).map(Into::into)
}

#[pyfunction]
pub fn run_query_simple(
    py: Python<'_>,
    db_url: String,
    query: String,
    use_cache: bool,
) -> PyResult<PyObject> {
    let empty_list = PyList::empty(py);
    run_manual_query_with_params(py, db_url, query, empty_list, use_cache)
}

#[pyfunction]
pub fn insert_data(py: Python<'_>, db_url: String, table_name: String, data: &PyDict, use_cache: bool) -> PyResult<PyObject> {
    // Validate database type
    get_db_type(&db_url)?;
    
    let data_map = py_dict_to_json(data)?;
    let locals = TaskLocals::with_running_loop(py)?;
    
    let fut = async move {
        let pool = get_or_create_pool(&db_url, use_cache).await.map_err(sqlx_err_to_py)?;
        
        // Generate column names and values for INSERT
        let columns: Vec<String> = data_map.keys().cloned().collect();
        let values: Vec<JsonValue> = columns.iter().map(|k| data_map[k].clone()).collect();
        
        // Build the INSERT query
        let placeholders: Vec<String> = (1..=values.len()).map(|i| format!("${}", i)).collect();
        let query = format!(
            "INSERT INTO {} ({}) VALUES ({}) RETURNING *",
            table_name,
            columns.join(", "),
            placeholders.join(", ")
        );
        
        let mut query_builder = sqlx::query(&query);
        
        // Bind parameters
        for value in values {
            match value {
                JsonValue::Null => query_builder = query_builder.bind(None::<String>),
                JsonValue::Bool(b) => query_builder = query_builder.bind(b),
                JsonValue::Number(n) => {
                    if let Some(i) = n.as_i64() {
                        query_builder = query_builder.bind(i);
                    } else if let Some(f) = n.as_f64() {
                        query_builder = query_builder.bind(f);
                    }
                },
                JsonValue::String(s) => query_builder = query_builder.bind(s),
                _ => {}
            }
        }
        
        // Execute the query and process results
        let rows = query_builder.fetch_all(&pool).await.map_err(sqlx_err_to_py)?;
        
        Python::with_gil(|py| {
            let py_list = PyList::empty(py);
            for row in rows {
                let py_dict = PyDict::new(py);
                for (i, column) in row.columns().iter().enumerate() {
                    let name = column.name();
                    let value = if let Ok(val) = row.try_get::<Option<String>, _>(i) {
                        match val {
                            Some(v) => v.into_py(py),
                            None => py.None()
                        }
                    } else if let Ok(val) = row.try_get::<Option<i64>, _>(i) {
                        match val {
                            Some(v) => v.into_py(py),
                            None => py.None()
                        }
                    } else if let Ok(val) = row.try_get::<Option<f64>, _>(i) {
                        match val {
                            Some(v) => v.into_py(py),
                            None => py.None()
                        }
                    } else {
                        py.None()
                    };
                    py_dict.set_item(name, value)?;
                }
                py_list.append(py_dict)?;
            }
            Ok::<Py<PyAny>, PyErr>(py_list.into_py(py))
        })
    };

    pyo3_asyncio::tokio::future_into_py_with_locals::<_, Py<PyAny>>(py, locals, fut).map(Into::into)
}

#[pyfunction]
pub fn update_data(py: Python<'_>, db_url: String, _table_name: String, data: &PyDict, filters: &PyDict, use_cache: bool) -> PyResult<PyObject> {
    let _data_map = py_dict_to_json(data)?;
    let _filters_map = py_dict_to_json(filters)?;
    let locals = TaskLocals::with_running_loop(py)?;
    
    let fut = async move {
        let _pool = get_or_create_pool(&db_url, use_cache).await.map_err(sqlx_err_to_py)?;
        // ...existing update implementation...
        Python::with_gil(|py| Ok::<Py<PyAny>, PyErr>(PyList::empty(py).into_py(py)))
    };

    pyo3_asyncio::tokio::future_into_py_with_locals::<_, Py<PyAny>>(py, locals, fut).map(Into::into)
}

#[pyfunction]
pub fn delete_data(py: Python<'_>, db_url: String, _table_name: String, filters: &PyDict, use_cache: bool) -> PyResult<PyObject> {
    let _filters_map = py_dict_to_json(filters)?;
    let locals = TaskLocals::with_running_loop(py)?;
    
    let fut = async move {
        let _pool = get_or_create_pool(&db_url, use_cache).await.map_err(sqlx_err_to_py)?;
        // ...existing delete implementation...
        Python::with_gil(|py| Ok::<Py<PyAny>, PyErr>(PyList::empty(py).into_py(py)))
    };

    pyo3_asyncio::tokio::future_into_py_with_locals::<_, Py<PyAny>>(py, locals, fut).map(Into::into)
}

// Helper function to convert Python dict to JSON Value
fn py_dict_to_json(dict: &PyDict) -> PyResult<HashMap<String, JsonValue>> {
    let mut result = HashMap::new();
    for (key, value) in dict.iter() {
        let key = key.extract::<String>()?;
        let value = if value.is_none() {
            JsonValue::Null
        } else if let Ok(s) = value.extract::<String>() {
            JsonValue::String(s)
        } else if let Ok(i) = value.extract::<i64>() {
            JsonValue::Number(i.into())
        } else if let Ok(f) = value.extract::<f64>() {
            JsonValue::Number(json!(f).as_number().unwrap().clone())
        } else {
            JsonValue::Null
        };
        result.insert(key, value);
    }
    Ok(result)
}