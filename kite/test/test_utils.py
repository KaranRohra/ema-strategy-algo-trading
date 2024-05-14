import datetime as dt
import pytz

from kite import utils


def test_get_instrument_token():
    assert utils.get_instrument_token("NSE", "INFY") == 408065


def test_get_symbol_holding():
    assert utils.get_symbol_holding("INFY") is None


def test_get_historical_data():
    historical_data = utils.get_historical_data("NSE", "INFY")
    now = dt.datetime.now(pytz.timezone("Asia/Kolkata"))
    candle_time = now.replace(
        minute=now.minute - now.minute % 5, second=0, microsecond=0
    )
    assert historical_data[-1]["date"] == candle_time


def test_get_current_ohlc():
    ohlc = utils.get_current_ohlc("NSE", "INFY")
    assert "open" in ohlc.keys()
    assert "high" in ohlc.keys()
    assert "low" in ohlc.keys()
    assert "close" in ohlc.keys()
