import ta.trend as trend
import pandas as pd
from datetime import datetime as dt, timedelta as td

from backtest import get_historical_data_for_back_testing
from signals import get_trend_analysis as gta


def dump_historical_data():
    historical_data = get_historical_data_for_back_testing(
        "NSE", "NIFTY BANK", dt(2015, 1, 1), dt(2024, 5, 10)
    )

    for h in historical_data:
        h["date"] = str(h["date"])

    pd.DataFrame(historical_data).to_csv(
        "./analysis/historical_data/historical_data_for_2015_to_2024_04.csv",
        index=False,
    )


def dump_data():
    analysis_lst = pd.read_csv("./analysis/final_candle_analysis.csv").to_dict(
        "records"
    )
    for i in range(len(analysis_lst)):
        analysis_lst[i]["date"] = analysis_lst[i]["date"].replace("+05:30", "")
        print(f"Completed {i}/{len(analysis_lst)} candles")

    pd.DataFrame(analysis_lst).to_csv(
        "./analysis/final_candle_analysis.csv", index=False
    )


def dump_trend(ema_value):
    historical_data = pd.read_csv("./analysis/historical_data.csv").to_dict("records")
    analysis_lst = []
    for i in range(1000, len(historical_data)):
        ema = trend.ema_indicator(
            pd.Series([c["close"] for c in historical_data[i - 1000: i + 1]]),
            window=ema_value,
        ).tolist()
        key = "ema" + str(ema_value)
        analysis_lst.append(
            {
                **historical_data[i],
                key: ema[-1],
                **gta(ema, "uptrend", key),
                **gta(ema, "downtrend", key),
            }
        )
        print(f"Completed {i}/{len(historical_data)} candles")
    pd.DataFrame(analysis_lst).to_csv(
        f"./analysis/candles/ema{ema_value}_trend.csv", index=False
    )


def combine_and_dump_all():
    final_data = []
    ema20_data = pd.read_csv("./analysis/candles/ema20_trend.csv").to_dict("records")
    ema50_data = pd.read_csv("./analysis/candles/ema50_trend.csv").to_dict("records")
    ema100_data = pd.read_csv("./analysis/candles/ema100_trend.csv").to_dict("records")
    ema200_data = pd.read_csv("./analysis/candles/ema200_trend.csv").to_dict("records")
    for i in range(len(ema20_data)):
        final_data.append(
            {
                **ema20_data[i],
                **ema50_data[i],
                **ema100_data[i],
                **ema200_data[i],
            }
        )
        print(f"Completed {i}/{len(ema20_data)} candles")
    
    pd.DataFrame(final_data).to_csv("./analysis/final_candle_analysis.csv", index=False)


combine_and_dump_all()