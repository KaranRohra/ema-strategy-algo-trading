import datetime as dt
import pandas as pd
import backtest.strategies as st

from connection import kite
from utils import kite_utils as ktu


def search_entry(exchange, symbol, ohlc, holdings, strategy_func, account_value):
    analysis = strategy_func(ohlc)
    curr = ohlc[-1]
    signal = analysis["signal"]
    trade = {
        "tradingsymbol": symbol,
        "exchange": exchange,
        "from": curr["date"],
        "entry_price": curr["close"],
        **analysis,
    }
    if signal == kite.TRANSACTION_TYPE_BUY:
        trade["quantity"] = account_value //( curr["close"] * 0.2)
        holdings.append(trade)
        print("Entered long position")
    elif signal == kite.TRANSACTION_TYPE_SELL:
        trade["quantity"] = -(account_value // (curr["close"] * 0.2))
        holdings.append(trade)
        print("Entered short position")


def search_exit(exchange, symbol, ohlc, holding, trades):
    curr = ohlc[-1]
    holding["exit_price"] = curr["close"]
    holding["to"] = curr["date"]

    if holding["quantity"] > 0 and curr["close"] < curr["ema200"]:
        holding["transaction_type"] = kite.TRANSACTION_TYPE_SELL
        holding["profit"] = holding["quantity"] * (
            holding["exit_price"] - holding["entry_price"]
        )
        trades.append(holding)
        print("Exited long position")
        return True
    elif holding["quantity"] < 0 and curr["close"] > curr["ema200"]:
        holding["transaction_type"] = kite.TRANSACTION_TYPE_BUY
        holding["profit"] = (-holding["quantity"]) * (
            holding["entry_price"] - holding["exit_price"]
        )
        trades.append(holding)
        print("Exited short position")
        return True


def get_historical_data_for_back_testing(
    instrument_token, from_date, to_date, interval="5minute"
):
    start_date = dt.datetime(from_date.year, from_date.month, from_date.day, 0, 0)
    end_date = start_date + dt.timedelta(days=98)

    historical_data = []

    while end_date <= to_date:
        historical_data.extend(
            kite.historical_data(
                instrument_token,
                from_date=start_date,
                to_date=end_date,
                interval=interval,
            )
        )
        print(f"Historical data fetched... for: {start_date} to {end_date}")
        start_date = end_date + dt.timedelta(days=1)
        end_date += dt.timedelta(days=97)

    if end_date > to_date:
        print(f"Historical data fetched... for: {start_date} to {end_date}")
        historical_data.extend(
            kite.historical_data(
                instrument_token,
                from_date=start_date,
                to_date=end_date,
                interval=interval,
            )
        )
    print(historical_data[:5])

    return historical_data


def start(exchange, symbol, strategy_func):
    ohlc = pd.read_csv("./analysis/nifty50/final_candle_analysis.csv").to_dict("records")
    candle_index = 250
    account_value = 100000
    holdings, trades = [], []
    while candle_index < len(ohlc):
        candles = ohlc[candle_index - 250 : candle_index + 1]
        holding = [h for h in holdings if h["tradingsymbol"] == symbol]
        if holding:
            if search_exit(exchange, symbol, candles, holding[0], trades):
                account_value += holding[0]["profit"]
                trades[-1]["account_value"] = account_value
                holdings = [h for h in holdings if h["tradingsymbol"] != symbol]
        else:
            search_entry(
                exchange, symbol, candles, holdings, strategy_func, account_value
            )

        candle_index += 1
        print(f"Completed {candle_index}/{len(ohlc)} candles")
    print(holdings)
    return trades


if __name__ == "__main__":
    exchange, symbol = "NSE", "NIFTY 50"
    strategy = input("Enter the strategy to backtest: ")
    file_name = strategy + "_" + symbol
    trades = start(
        exchange,
        symbol,
        getattr(st, strategy),
    )

    csv_path = "./analysis/nifty50/" + file_name + ".csv"
    for i in range(len(trades)):
        trades[i]["index"] = i
        trades[i]["strategy"] = file_name
    pd.DataFrame(trades).to_csv(csv_path, index=False)
