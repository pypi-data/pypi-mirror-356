use karva_project::path::SystemPathBuf;
use pyo3::{PyResult, Python, types::PyAnyMethods};
use ruff_python_ast::PythonVersion;
use ruff_source_file::{LineIndex, PositionEncoding};
use ruff_text_size::TextSize;

#[must_use]
pub fn current_python_version() -> PythonVersion {
    PythonVersion::from(Python::with_gil(|py| {
        let inferred_python_version = py.version_info();
        (inferred_python_version.major, inferred_python_version.minor)
    }))
}

#[must_use]
pub fn from_text_size(offset: TextSize, source: &str) -> (usize, usize) {
    let index = LineIndex::from_source_text(source);
    let location = index.source_location(offset, source, PositionEncoding::Utf8);
    (location.line.get(), location.character_offset.get())
}

pub fn recursive_add_to_sys_path(
    py: Python<'_>,
    path: &SystemPathBuf,
    cwd: &SystemPathBuf,
) -> PyResult<()> {
    let sys = py.import("sys")?;
    let sys_path = sys.getattr("path")?;
    let path = path.as_std_path();
    let cwd = cwd.as_std_path();

    let mut current = cwd;
    while current != path && path.starts_with(current) {
        sys_path.call_method1("append", (current.display().to_string(),))?;
        if let Some(parent) = current.parent() {
            current = parent;
        } else {
            break;
        }
    }

    if current != path {
        sys_path.call_method1("append", (path.display().to_string(),))?;
    }
    Ok(())
}

pub fn add_to_sys_path(py: &Python<'_>, path: &SystemPathBuf) -> PyResult<()> {
    let sys_path = py.import("sys")?;
    let sys_path = sys_path.getattr("path")?;
    sys_path.call_method1("append", (path.as_std_path().display().to_string(),))?;
    Ok(())
}

pub trait Upcast<T> {
    fn upcast(self) -> T;
}

impl<T> Upcast<T> for T {
    fn upcast(self) -> T {
        self
    }
}

pub fn set_output(py: Python<'_>, show_output: bool) -> PyResult<()> {
    if !show_output {
        let sys = py.import("sys")?;
        let os = py.import("os")?;
        let builtins = py.import("builtins")?;
        let logging = py.import("logging")?;

        let devnull = os.getattr("devnull")?;
        let open_file_function = builtins.getattr("open")?;
        let null_file = open_file_function.call1((devnull, "w"))?;

        for output in ["stdout", "stderr"] {
            sys.setattr(output, null_file.clone())?;
        }

        logging.call_method1("disable", (logging.getattr("CRITICAL")?,))?;
    }
    Ok(())
}
