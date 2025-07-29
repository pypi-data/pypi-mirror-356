#[pyfunction]
pub fn begin_transaction(py: Python, db_url: String, use_cache: bool) -> PyResult<PyObject> {
    let fut = async move {
        let pool = get_or_create_pool(&db_url, use_cache).await?;
        let tx = pool.begin().await?;
        let boxed = Box::new(tx);
        let tx_ptr = Box::into_raw(boxed) as usize;
        Ok(json!({ "tx_id": tx_ptr }))
    };
    pyo3_asyncio::tokio::into_coroutine(py, fut)
}

#[pyfunction]
pub fn commit_transaction(py: Python, tx_id: usize) -> PyResult<PyObject> {
    let fut = async move {
        let tx_ptr = tx_id as *mut sqlx::Transaction<'static, sqlx::Any>;
        if tx_ptr.is_null() {
            return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid transaction ID"));
        }

        let boxed_tx = unsafe { Box::from_raw(tx_ptr) };
        boxed_tx.commit().await?;
        Ok(json!({ "status": "committed" }))
    };
    pyo3_asyncio::tokio::into_coroutine(py, fut)
}

#[pyfunction]
pub fn rollback_transaction(py: Python, tx_id: usize) -> PyResult<PyObject> {
    let fut = async move {
        let tx_ptr = tx_id as *mut sqlx::Transaction<'static, sqlx::Any>;
        if tx_ptr.is_null() {
            return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid transaction ID"));
        }

        let boxed_tx = unsafe { Box::from_raw(tx_ptr) };
        boxed_tx.rollback().await?;
        Ok(json!({ "status": "rolled_back" }))
    };
    pyo3_asyncio::tokio::into_coroutine(py, fut)
}
