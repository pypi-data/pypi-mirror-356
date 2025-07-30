/*
    BSD 3-Clause License

    Copyright (c) 2025, Guillaume GOBIN (Guitheg)

    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation and/or
    other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its contributors
    may be used to endorse or promote products derived from this software without
    specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
    THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
/*
    List of contributors:
    - Guitheg: Initial implementation
*/

use numpy::{IntoPyArray, PyArray1, PyArrayMethods, PyUntypedArrayMethods};
use pyo3::{exceptions::PyValueError, pyclass, pyfunction, pymethods, Py, PyResult, Python};
use techalib::indicators::rsi::{rsi_into, RsiState};
use techalib::traits::State;
use techalib::types::Float;

#[pyclass(name = "RsiState")]
#[derive(Debug, Clone)]
pub struct PyRsiState {
    #[pyo3(get)]
    pub rsi: Float,
    #[pyo3(get)]
    pub prev_value: Float,
    #[pyo3(get)]
    pub avg_gain: Float,
    #[pyo3(get)]
    pub avg_loss: Float,
    #[pyo3(get)]
    pub period: usize,
}

#[pymethods]
impl PyRsiState {
    #[new]
    pub fn new(
        rsi: Float,
        prev_value: Float,
        avg_gain: Float,
        avg_loss: Float,
        period: usize,
    ) -> Self {
        PyRsiState {
            rsi,
            prev_value,
            avg_gain,
            avg_loss,
            period,
        }
    }

    #[getter]
    pub fn __str__(&self) -> String {
        self.__repr__()
    }
    #[getter]
    pub fn __repr__(&self) -> String {
        format!("{:?}", self)
    }
}

impl From<RsiState> for PyRsiState {
    fn from(state: RsiState) -> Self {
        PyRsiState {
            rsi: state.rsi,
            prev_value: state.prev_value,
            avg_gain: state.avg_gain,
            avg_loss: state.avg_loss,
            period: state.period,
        }
    }
}

impl From<PyRsiState> for RsiState {
    fn from(py_state: PyRsiState) -> Self {
        RsiState {
            rsi: py_state.rsi,
            prev_value: py_state.prev_value,
            avg_gain: py_state.avg_gain,
            avg_loss: py_state.avg_loss,
            period: py_state.period,
        }
    }
}

#[pyfunction(signature = (data, period = 14, release_gil = false))]
pub(crate) fn rsi(
    py: Python,
    data: numpy::PyReadonlyArray1<Float>,
    period: usize,
    release_gil: bool,
) -> PyResult<(Py<PyArray1<Float>>, PyRsiState)> {
    let len: usize = data.len();
    let input_slice = data.as_slice()?;

    if release_gil {
        let mut output = vec![0.0; len];
        let rsi_state = py
            .allow_threads(|| rsi_into(input_slice, period, output.as_mut_slice()))
            .map_err(|e| PyValueError::new_err(format!("{:?}", e)))?;

        return Ok((output.into_pyarray(py).into(), rsi_state.into()));
    } else {
        let output_array = PyArray1::<Float>::zeros(py, [len], false);
        let output_slice = unsafe { output_array.as_slice_mut()? };

        let rsi_state = rsi_into(input_slice, period, output_slice)
            .map_err(|e| PyValueError::new_err(format!("{:?}", e)))?;

        return Ok((output_array.into(), rsi_state.into()));
    }
}

#[pyfunction(signature = (new_value, rsi_state))]
pub(crate) fn rsi_next(new_value: Float, rsi_state: PyRsiState) -> PyResult<PyRsiState> {
    let mut state: RsiState = rsi_state.into();
    state
        .update(new_value)
        .map_err(|e| PyValueError::new_err(format!("{:?}", e)))?;
    Ok(state.into())
}
