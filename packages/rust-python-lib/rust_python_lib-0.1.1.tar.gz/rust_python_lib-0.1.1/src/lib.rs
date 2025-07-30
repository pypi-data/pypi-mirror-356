use std::fmt::format;

use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// 一个用 Rust 实现的、性能很高的斐波那契函数
#[pyfunction]
fn fibonacci(n: u64) -> PyResult<u64> {
    if n <= 1 {
        return Ok(n);
    }
    let mut a = 0;
    let mut b = 1;
    for _ in 2..=n {
        let next = a + b;
        a = b;
        b = next;
    }
    Ok(b)
}

/// 一个hello world test
#[pyfunction]
fn hello_world(name: String) -> PyResult<String> {
    let result = format!("Hello, {}.I'm LiXin.It's nice to see you again",name);
    Ok(result)
}

/// A Python module implemented in Rust.
#[pymodule]
fn rust_python_lib(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(fibonacci, m)?)?;
    m.add_function(wrap_pyfunction!(hello_world, m)?)?;
    Ok(())
}
