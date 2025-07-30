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

use numpy::{IntoPyArray, PyArray1, PyArrayMethods, PyReadonlyArray1, PyUntypedArrayMethods};
use pyo3::{exceptions::PyValueError, pyclass, pyfunction, pymethods, Py, PyResult, Python};
use techalib::indicators::bbands::{
    bbands_into, BBandsMA, BBandsState, DeviationMulipliers, MovingAverageState,
};
use techalib::traits::State;
use techalib::types::Float;

#[pyclass(name = "BBandsState")]
#[derive(Debug, Clone)]
pub struct PyBBandsState {
    #[pyo3(get)]
    pub upper: Float,
    #[pyo3(get)]
    pub middle: Float,
    #[pyo3(get)]
    pub lower: Float,
    #[pyo3(get)]
    pub mean_sma: Float,
    #[pyo3(get)]
    pub mean_sq: Float,
    #[pyo3(get)]
    pub window: Vec<Float>,
    #[pyo3(get)]
    pub period: usize,
    #[pyo3(get)]
    pub std_up: Float,
    #[pyo3(get)]
    pub std_down: Float,
    #[pyo3(get)]
    pub ma_type: PyBBandsMA,
}

#[pyclass(name = "BBandsMA")]
#[derive(Debug, Clone, Copy)]
pub enum PyBBandsMA {
    SMA,
    EMA,
}

#[pymethods]
impl PyBBandsState {
    #[new]
    pub fn new(
        upper: Float,
        middle: Float,
        lower: Float,
        mean_sma: Float,
        mean_sq: Float,
        window: Vec<Float>,
        period: usize,
        std_up: Float,
        std_down: Float,
        ma_type: PyBBandsMA,
    ) -> Self {
        PyBBandsState {
            upper,
            middle,
            lower,
            mean_sma,
            mean_sq,
            window,
            period,
            std_up,
            std_down,
            ma_type,
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
impl From<BBandsState> for PyBBandsState {
    fn from(state: BBandsState) -> Self {
        PyBBandsState {
            upper: state.upper,
            middle: state.middle,
            lower: state.lower,
            mean_sma: state.moving_averages.sma,
            mean_sq: state.moving_averages.ma_square,
            window: state.last_window.into(),
            period: state.period,
            std_up: state.std_dev_mult.up,
            std_down: state.std_dev_mult.down,
            ma_type: state.ma_type.into(),
        }
    }
}

impl From<PyBBandsState> for BBandsState {
    fn from(py_state: PyBBandsState) -> Self {
        BBandsState {
            upper: py_state.upper,
            middle: py_state.middle,
            lower: py_state.lower,
            moving_averages: MovingAverageState {
                sma: py_state.mean_sma,
                ma_square: py_state.mean_sq,
            },
            last_window: py_state.window.into(),
            period: py_state.period,
            std_dev_mult: DeviationMulipliers {
                up: py_state.std_up,
                down: py_state.std_down,
            },
            ma_type: py_state.ma_type.into(),
        }
    }
}

impl From<PyBBandsMA> for BBandsMA {
    fn from(py_ma: PyBBandsMA) -> Self {
        match py_ma {
            PyBBandsMA::SMA => BBandsMA::SMA,
            PyBBandsMA::EMA => BBandsMA::EMA(None),
        }
    }
}

impl From<BBandsMA> for PyBBandsMA {
    fn from(ma: BBandsMA) -> Self {
        match ma {
            BBandsMA::SMA => PyBBandsMA::SMA,
            BBandsMA::EMA(_) => PyBBandsMA::EMA,
        }
    }
}

#[pyfunction(signature = (data, period = 20, std_up = 2.0, std_down = 2.0, ma_type = PyBBandsMA::SMA, release_gil = false))]
pub(crate) fn bbands(
    py: Python,
    data: PyReadonlyArray1<Float>,
    period: usize,
    std_up: Float,
    std_down: Float,
    ma_type: PyBBandsMA,
    release_gil: bool,
) -> PyResult<(
    Py<PyArray1<Float>>,
    Py<PyArray1<Float>>,
    Py<PyArray1<Float>>,
    PyBBandsState,
)> {
    let len = data.len();
    let input_slice = data.as_slice()?;

    if release_gil {
        let mut output_upper = vec![0.0; len];
        let mut output_middle = vec![0.0; len];
        let mut output_lower = vec![0.0; len];

        let state = py
            .allow_threads(|| {
                bbands_into(
                    input_slice,
                    period,
                    DeviationMulipliers {
                        up: std_up,
                        down: std_down,
                    },
                    ma_type.into(),
                    output_upper.as_mut_slice(),
                    output_middle.as_mut_slice(),
                    output_lower.as_mut_slice(),
                )
            })
            .map_err(|e| PyValueError::new_err(format!("{:?}", e)))?;

        Ok((
            output_upper.into_pyarray(py).into(),
            output_middle.into_pyarray(py).into(),
            output_lower.into_pyarray(py).into(),
            state.into(),
        ))
    } else {
        let py_out_upper = PyArray1::<Float>::zeros(py, [len], false);
        let py_out_upper_slice = unsafe { py_out_upper.as_slice_mut()? };

        let py_out_middle = PyArray1::<Float>::zeros(py, [len], false);
        let py_out_middle_slice = unsafe { py_out_middle.as_slice_mut()? };

        let py_out_lower = PyArray1::<Float>::zeros(py, [len], false);
        let py_out_lower_slice = unsafe { py_out_lower.as_slice_mut()? };

        let state = bbands_into(
            input_slice,
            period,
            DeviationMulipliers {
                up: std_up,
                down: std_down,
            },
            ma_type.into(),
            py_out_upper_slice,
            py_out_middle_slice,
            py_out_lower_slice,
        )
        .map_err(|e| PyValueError::new_err(format!("{:?}", e)))?;

        Ok((
            py_out_upper.into(),
            py_out_middle.into(),
            py_out_lower.into(),
            state.into(),
        ))
    }
}

#[pyfunction(signature = (new_value, bbands_state))]
pub(crate) fn bbands_next(
    new_value: Float,
    bbands_state: PyBBandsState,
) -> PyResult<PyBBandsState> {
    let mut bbands_state: BBandsState = bbands_state.into();
    bbands_state
        .update(new_value)
        .map_err(|e| PyValueError::new_err(format!("{:?}", e)))?;

    Ok(bbands_state.into())
}
