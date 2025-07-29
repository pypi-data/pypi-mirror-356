import json
from unittest.mock import MagicMock, patch

import pytest

import openmarkets.tools.options as opt


@pytest.mark.asyncio
@patch("yfinance.Ticker")
async def test_get_options_expiration_dates_success(mock_ticker_cls):
    mock_ticker = MagicMock()
    mock_ticker.options = ["2024-06-21", "2024-06-28"]
    mock_ticker_cls.return_value = mock_ticker

    result = await opt.get_options_expiration_dates("AAPL")
    data = json.loads(result)
    assert "expiration_dates" in data
    assert data["expiration_dates"] == ["2024-06-21", "2024-06-28"]


@pytest.mark.xfail
@pytest.mark.asyncio
@patch("yfinance.Ticker")
async def test_get_options_expiration_dates_error(mock_ticker_cls):
    mock_ticker_cls.side_effect = Exception("fail")
    result = await opt.get_options_expiration_dates("AAPL")
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
@patch("yfinance.Ticker")
async def test_get_option_chain_success(mock_ticker_cls):
    mock_calls = MagicMock()
    mock_calls.to_dict.return_value = [{"strike": 100}]
    mock_puts = MagicMock()
    mock_puts.to_dict.return_value = [{"strike": 90}]
    mock_chain = MagicMock(calls=mock_calls, puts=mock_puts)
    mock_ticker = MagicMock()
    mock_ticker.options = ["2024-06-21"]
    mock_ticker.option_chain.return_value = mock_chain
    mock_ticker_cls.return_value = mock_ticker

    result = await opt.get_option_chain("AAPL", "2024-06-21")
    data = json.loads(result)
    assert "calls" in data and "puts" in data


@pytest.mark.asyncio
@patch("yfinance.Ticker")
async def test_get_option_chain_no_expirations(mock_ticker_cls):
    mock_ticker = MagicMock()
    mock_ticker.options = []
    mock_ticker_cls.return_value = mock_ticker

    result = await opt.get_option_chain("AAPL")
    data = json.loads(result)
    assert "error" in data


@pytest.mark.asyncio
@patch("yfinance.Ticker")
async def test_get_options_volume_analysis_success(mock_ticker_cls):
    import pandas as pd

    calls = pd.DataFrame({"volume": [10, 20], "openInterest": [100, 200]})
    puts = pd.DataFrame({"volume": [5, 15], "openInterest": [50, 150]})
    mock_chain = MagicMock(calls=calls, puts=puts)
    mock_ticker = MagicMock()
    mock_ticker.options = ["2024-06-21"]
    mock_ticker.option_chain.return_value = mock_chain
    mock_ticker_cls.return_value = mock_ticker

    result = await opt.get_options_volume_analysis("AAPL", "2024-06-21")
    data = json.loads(result)
    assert "total_call_volume" in data
    assert data["total_call_volume"] == 30
    assert data["total_put_volume"] == 20


@pytest.mark.asyncio
@patch("yfinance.Ticker")
async def test_get_options_by_moneyness_success(mock_ticker_cls):
    import pandas as pd

    calls = pd.DataFrame({"strike": [95, 100, 105]})
    puts = pd.DataFrame({"strike": [90, 100, 110]})
    mock_chain = MagicMock(calls=calls, puts=puts)
    mock_ticker = MagicMock()
    mock_ticker.options = ["2024-06-21"]
    mock_ticker.option_chain.return_value = mock_chain
    mock_ticker.info = {"currentPrice": 100}
    mock_ticker_cls.return_value = mock_ticker

    result = await opt.get_options_by_moneyness("AAPL", moneyness_range=0.05)
    data = json.loads(result)
    assert "calls" in data and "puts" in data
    assert all(95 <= c["strike"] <= 105 for c in data["calls"])
    assert all(95 <= p["strike"] <= 105 for p in data["puts"])


@pytest.mark.asyncio
@patch("yfinance.Ticker")
async def test_get_options_by_moneyness_no_price(mock_ticker_cls):
    mock_chain = MagicMock(calls=[], puts=[])
    mock_ticker = MagicMock()
    mock_ticker.options = ["2024-06-21"]
    mock_ticker.option_chain.return_value = mock_chain
    mock_ticker.info = {}
    mock_ticker_cls.return_value = mock_ticker

    result = await opt.get_options_by_moneyness("AAPL")
    data = json.loads(result)
    assert "error" in data
