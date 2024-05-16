import os
import datetime as dt
import pandas as pd
import strategies as st

from kite import utils as ktu
from constants import kite


def search_entry(exchange, symbol, ohlc, holdings, strategy_func):
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
        trade["quantity"] = 1
        trade["signal"] = "BUY"
        holdings.append(trade)
        print("Entered long position")
    elif signal == kite.TRANSACTION_TYPE_SELL:
        trade["quantity"] = -1
        trade["signal"] = "SELL"
        holdings.append(trade)
        print("Entered short position")


def search_exit(exchange, symbol, ohlc, holding, trades):
    curr = ohlc[-1]
    holding["exit_price"] = curr["close"]
    holding["to"] = curr["date"]

    if holding["quantity"] > 0 and curr["close"] < curr["ema200"]:
        holding["transaction_type"] = kite.TRANSACTION_TYPE_SELL
        trades.append(holding)
        print("Exited long position")
        return True
    elif holding["quantity"] < 0 and curr["close"] > curr["ema200"]:
        holding["transaction_type"] = kite.TRANSACTION_TYPE_BUY
        trades.append(holding)
        print("Exited short position")
        return True


def get_historical_data_for_back_testing(exchange, symbol, from_date, to_date):
    start_date = dt.datetime(from_date.year, from_date.month, from_date.day, 0, 0)
    end_date = start_date + dt.timedelta(days=98)

    historical_data = []

    while end_date <= to_date:
        historical_data.extend(
            ktu.get_historical_data(
                exchange, symbol, from_date=start_date, to_date=end_date
            )
        )
        print(f"Historical data fetched... for: {start_date} to {end_date}")
        start_date = end_date + dt.timedelta(days=1)
        end_date += dt.timedelta(days=97)

    if end_date > to_date:
        print(f"Historical data fetched... for: {start_date} to {end_date}")
        historical_data.extend(
            ktu.get_historical_data(
                exchange, symbol, from_date=start_date, to_date=to_date
            )
        )
    print(historical_data[:5])

    return historical_data


def start(exchange, symbol, strategy_func):
    ohlc = pd.read_csv("./analysis/final_candle_analysis.csv").to_dict("records")
    candle_index = 250
    holdings, trades = [], []
    while candle_index < len(ohlc):
        candles = ohlc[candle_index - 250 : candle_index + 1]
        holding = [h for h in holdings if h["tradingsymbol"] == symbol]
        if holding:
            if search_exit(exchange, symbol, candles, holding[0], trades):
                holdings = [h for h in holdings if h["tradingsymbol"] != symbol]
        else:
            search_entry(exchange, symbol, candles, holdings, strategy_func)

        candle_index += 1
        print(f"Completed {candle_index}/{len(ohlc)} candles")
    return trades


if __name__ == "__main__":
    exchange, symbol = os.environ["EXCHANGE"], os.environ["SYMBOL"]
    strategy = input("Enter the strategy to backtest: ")
    trades = start(
        exchange,
        symbol,
        getattr(st, strategy),
    )

    csv_path = "./analysis/" + strategy + ".csv"
    for i in range(len(trades)):
        trades[i]["index"] = i
        trades[i]["strategy"] = strategy
    pd.DataFrame(trades).to_csv(csv_path, index=False)
