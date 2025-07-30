use pyo3::prelude::*;

mod py_ad;
mod py_adx;
mod py_aroon;
mod py_aroonosc;
mod py_atr;
mod py_bbands;
mod py_dema;
mod py_dx;
mod py_ema;
mod py_kama;
mod py_macd;
mod py_midpoint;
mod py_midprice;
mod py_minus_di;
mod py_minus_dm;
mod py_plus_di;
mod py_plus_dm;
mod py_roc;
mod py_rocr;
mod py_rsi;
mod py_sma;
mod py_t3;
mod py_tema;
mod py_trima;
mod py_wma;

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_ema::ema, m)?)?;
    m.add_function(wrap_pyfunction!(py_ema::ema_next, m)?)?;
    m.add_class::<py_ema::PyEmaState>()?;

    m.add_function(wrap_pyfunction!(py_rsi::rsi, m)?)?;
    m.add_function(wrap_pyfunction!(py_rsi::rsi_next, m)?)?;
    m.add_class::<py_rsi::PyRsiState>()?;

    m.add_function(wrap_pyfunction!(py_sma::sma, m)?)?;
    m.add_function(wrap_pyfunction!(py_sma::sma_next, m)?)?;
    m.add_class::<py_sma::PySmaState>()?;

    m.add_function(wrap_pyfunction!(py_macd::macd, m)?)?;
    m.add_function(wrap_pyfunction!(py_macd::macd_next, m)?)?;
    m.add_class::<py_macd::PyMacdState>()?;

    m.add_function(wrap_pyfunction!(py_bbands::bbands, m)?)?;
    m.add_function(wrap_pyfunction!(py_bbands::bbands_next, m)?)?;
    m.add_class::<py_bbands::PyBBandsState>()?;
    m.add_class::<py_bbands::PyBBandsMA>()?;

    m.add_function(wrap_pyfunction!(py_wma::wma, m)?)?;
    m.add_function(wrap_pyfunction!(py_wma::wma_next, m)?)?;
    m.add_class::<py_wma::PyWmaState>()?;

    m.add_function(wrap_pyfunction!(py_dema::dema, m)?)?;
    m.add_function(wrap_pyfunction!(py_dema::dema_next, m)?)?;
    m.add_class::<py_dema::PyDemaState>()?;

    m.add_function(wrap_pyfunction!(py_tema::tema, m)?)?;
    m.add_function(wrap_pyfunction!(py_tema::tema_next, m)?)?;
    m.add_class::<py_tema::PyTemaState>()?;

    m.add_function(wrap_pyfunction!(py_trima::trima, m)?)?;
    m.add_function(wrap_pyfunction!(py_trima::trima_next, m)?)?;
    m.add_class::<py_trima::PyTrimaState>()?;

    m.add_function(wrap_pyfunction!(py_t3::t3, m)?)?;
    m.add_function(wrap_pyfunction!(py_t3::t3_next, m)?)?;
    m.add_class::<py_t3::PyT3State>()?;

    m.add_function(wrap_pyfunction!(py_kama::kama, m)?)?;
    m.add_function(wrap_pyfunction!(py_kama::kama_next, m)?)?;
    m.add_class::<py_kama::PyKamaState>()?;
    m.add_function(wrap_pyfunction!(py_midpoint::midpoint, m)?)?;
    m.add_function(wrap_pyfunction!(py_midpoint::midpoint_next, m)?)?;
    m.add_class::<py_midpoint::PyMidpointState>()?;
    m.add_function(wrap_pyfunction!(py_midprice::midprice, m)?)?;
    m.add_function(wrap_pyfunction!(py_midprice::midprice_next, m)?)?;
    m.add_class::<py_midprice::PyMidpriceState>()?;
    m.add_function(wrap_pyfunction!(py_roc::roc, m)?)?;
    m.add_function(wrap_pyfunction!(py_roc::roc_next, m)?)?;
    m.add_class::<py_roc::PyRocState>()?;
    m.add_function(wrap_pyfunction!(py_atr::atr, m)?)?;
    m.add_function(wrap_pyfunction!(py_atr::atr_next, m)?)?;
    m.add_class::<py_atr::PyAtrState>()?;
    m.add_function(wrap_pyfunction!(py_ad::ad, m)?)?;
    m.add_function(wrap_pyfunction!(py_ad::ad_next, m)?)?;
    m.add_class::<py_ad::PyAdState>()?;
    m.add_function(wrap_pyfunction!(py_minus_dm::minus_dm, m)?)?;
    m.add_function(wrap_pyfunction!(py_minus_dm::minus_dm_next, m)?)?;
    m.add_class::<py_minus_dm::PyMinusDmState>()?;
    m.add_function(wrap_pyfunction!(py_plus_dm::plus_dm, m)?)?;
    m.add_function(wrap_pyfunction!(py_plus_dm::plus_dm_next, m)?)?;
    m.add_class::<py_plus_dm::PyPlusDmState>()?;
    m.add_function(wrap_pyfunction!(py_minus_di::minus_di, m)?)?;
    m.add_function(wrap_pyfunction!(py_minus_di::minus_di_next, m)?)?;
    m.add_class::<py_minus_di::PyMinusDiState>()?;
    m.add_function(wrap_pyfunction!(py_plus_di::plus_di, m)?)?;
    m.add_function(wrap_pyfunction!(py_plus_di::plus_di_next, m)?)?;
    m.add_class::<py_plus_di::PyPlusDiState>()?;
    m.add_function(wrap_pyfunction!(py_dx::dx, m)?)?;
    m.add_function(wrap_pyfunction!(py_dx::dx_next, m)?)?;
    m.add_class::<py_dx::PyDxState>()?;
    m.add_function(wrap_pyfunction!(py_adx::adx, m)?)?;
    m.add_function(wrap_pyfunction!(py_adx::adx_next, m)?)?;
    m.add_class::<py_adx::PyAdxState>()?;
    m.add_function(wrap_pyfunction!(py_rocr::rocr, m)?)?;
    m.add_function(wrap_pyfunction!(py_rocr::rocr_next, m)?)?;
    m.add_class::<py_rocr::PyRocrState>()?;
    m.add_function(wrap_pyfunction!(py_aroon::aroon, m)?)?;
    m.add_function(wrap_pyfunction!(py_aroon::aroon_next, m)?)?;
    m.add_class::<py_aroon::PyAroonState>()?;
    m.add_function(wrap_pyfunction!(py_aroonosc::aroonosc, m)?)?;
    m.add_function(wrap_pyfunction!(py_aroonosc::aroonosc_next, m)?)?;
    m.add_class::<py_aroonosc::PyAroonoscState>()?;
    Ok(())
}
