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

/*
    Inspired by TA-LIB MIDPOINT implementation
*/

//! Middle point (MIDPOINT) implementation

use std::collections::VecDeque;

use crate::errors::TechalibError;
use crate::traits::State;
use crate::types::Float;

/// MIDPOINT calculation result
/// ---
/// This struct holds the result and the state ([`MidpointState`])
/// of the calculation.
///
/// Attributes
/// ---
/// - `midpoint`: A vector of [`Float`] representing the calculated MIDPOINT values.
/// - `state`: A [`MidpointState`], which can be used to calculate
///   the next values incrementally.
#[derive(Debug)]
pub struct MidpointResult {
    /// The calculated MIDPOINT values.
    pub midpoint: Vec<Float>,
    /// The [`MidpointState`] state of the MIDPOINT calculation.
    pub state: MidpointState,
}

/// MIDPOINT calculation state
/// ---
/// This struct holds the state of the calculation.
/// It is used to calculate the next values in a incremental way.
///
/// Attributes
/// ---
/// **Last outputs values**
/// - `midpoint`: The last calculated MIDPOINT value.
///
/// **State values**
/// - `last_window`: A deque containing the last `period` values used for the MIDPOINT calculation.
///
/// **Parameters**
/// - `period`: The period used for the MIDPOINT calculation.
#[derive(Debug, Clone)]
pub struct MidpointState {
    // Outputs
    /// The last calculated MIDPOINT value.
    pub midpoint: Float,

    // State values
    /// A deque containing the last `period` values used for the MIDPOINT calculation.
    pub last_window: VecDeque<Float>,

    // Parameters
    /// The period used for the MIDPOINT calculation, which determines
    pub period: usize,
}

impl State<Float> for MidpointState {
    /// Update the [`MidpointState`] with a new sample
    ///
    /// Input Arguments
    /// ---
    /// - `sample`: The new input to update the MIDPOINT state
    fn update(&mut self, sample: Float) -> Result<(), TechalibError> {
        check_finite!(sample);
        check_param_gte!(self.period, 2);
        if self.last_window.len() != self.period {
            return Err(TechalibError::BadParam(format!(
                "MIDPOINT state last_window length must be equal to period ({}), got: {}",
                self.period,
                self.last_window.len()
            )));
        }

        for (idx, &value) in self.last_window.iter().enumerate() {
            if !value.is_finite() {
                return Err(TechalibError::DataNonFinite(format!(
                    "last_window[{idx}] = {value:?}"
                )));
            }
        }

        let mut window = self.last_window.clone();

        let _ = window.pop_front().ok_or(TechalibError::InsufficientData)?;
        window.push_back(sample);

        let midpoint = midpoint_next_unchecked(window.make_contiguous());

        check_finite!(midpoint);
        self.last_window = window;
        self.midpoint = midpoint;

        Ok(())
    }
}

/// Lookback period for MIDPOINT calculation
/// ---
/// With `n = lookback_from_period(period)`,
/// the `n-1` first values that will be return will be `NaN`
/// The n-th value will be the first valid value,
#[inline(always)]
pub fn lookback_from_period(period: usize) -> Result<usize, TechalibError> {
    if period <= 1 {
        return Err(TechalibError::BadParam(format!(
            "Period must be greater than 1, got: {}",
            period
        )));
    }
    Ok(period - 1)
}

/// Calculation of the MIDPOINT function
/// ---
/// It returns a [`MidpointResult`]
///
/// Input Arguments
/// ---
/// - `data`: A slice of [`Float`] representing the input data.
/// - `period`: The period for the MIDPOINT calculation.
///
/// Returns
/// ---
/// A `Result` containing a [`MidpointResult`],
/// or a [`TechalibError`] error if the calculation fails.
pub fn midpoint(data: &[Float], period: usize) -> Result<MidpointResult, TechalibError> {
    let mut output = vec![0.0; data.len()];

    let midpoint_state = midpoint_into(data, period, output.as_mut_slice())?;

    Ok(MidpointResult {
        midpoint: output,
        state: midpoint_state,
    })
}

/// Calculation of the MIDPOINT function
/// ---
/// It stores the results in the provided output arrays and
/// return the state [`MidpointState`].
///
/// Input Arguments
/// ---
/// - `data`: A slice of [`Float`] representing the input data.
/// - `period`: The period for the MIDPOINT calculation.
///
/// Output Arguments
/// ---
/// - `output`: A mutable slice of [`Float`] where the calculated MIDPOINT values will be stored.
///
/// Returns
/// ---
/// A `Result` containing a [`MidpointState`],
/// or a [`TechalibError`] error if the calculation fails.
pub fn midpoint_into(
    data: &[Float],
    period: usize,
    output: &mut [Float],
) -> Result<MidpointState, TechalibError> {
    check_param_eq!(output.len(), data.len());
    let len = data.len();
    let lookback = lookback_from_period(period)?;

    if len <= lookback {
        return Err(TechalibError::InsufficientData);
    }

    let midpoint = init_midpoint_unchecked(data, lookback, output)?;
    output[lookback] = midpoint;
    check_finite_at!(lookback, output);

    for idx in lookback + 1..len {
        check_finite_at!(idx, data);
        output[idx] = midpoint_next_unchecked(&data[idx - lookback..=idx]);
        check_finite_at!(idx, output);
    }

    Ok(MidpointState {
        midpoint: output[len - 1],
        last_window: VecDeque::from(data[len - period..len].to_vec()),
        period,
    })
}

#[inline(always)]
fn init_midpoint_unchecked(
    data: &[Float],
    lookback: usize,
    output: &mut [Float],
) -> Result<Float, TechalibError> {
    check_finite_at!(0, data);
    let mut maximum = data[0];
    let mut minimum = maximum;
    output[0] = f64::NAN;
    for idx in 1..lookback {
        check_finite_at!(idx, data);
        (maximum, minimum) = minmax(data[idx], maximum, minimum);
        output[idx] = f64::NAN;
    }
    check_finite_at!(lookback, data);
    (maximum, minimum) = minmax(data[lookback], maximum, minimum);

    Ok(calculate_midpoint(maximum, minimum))
}

#[inline(always)]
fn midpoint_next_unchecked(last_window: &[Float]) -> Float {
    let mut maximum = last_window[0];
    let mut minimum = maximum;
    for j in last_window {
        (maximum, minimum) = minmax(*j, maximum, minimum);
    }
    calculate_midpoint(maximum, minimum)
}

#[inline(always)]
fn minmax(new_value: Float, maximum: Float, minimum: Float) -> (Float, Float) {
    if new_value < minimum {
        (maximum, new_value)
    } else if new_value > maximum {
        (new_value, minimum)
    } else {
        (maximum, minimum)
    }
}

const HALF: Float = 0.5;

#[inline(always)]
fn calculate_midpoint(maximum: Float, minimum: Float) -> Float {
    (maximum + minimum) * HALF
}
