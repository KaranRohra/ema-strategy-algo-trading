from connection import kite

def s7(ohlc: list):
    curr, n = ohlc[-1], len(ohlc)
    analysis = {
        "close_above_emas": curr["close"] > curr["ema50"] > curr["ema200"],
        "close_below_emas": curr["close"] < curr["ema50"] < curr["ema200"],
        **curr,
        "candle_cnt_close_above_ema50": 0,
        "candle_cnt_close_below_ema50": 0,
        "candle_cnt_ema50_above_ema200": 0,
        "candle_cnt_ema50_below_ema200": 0,
        "signal": None,
    }

    for i in range(n - 1, -1, -1):
        if ohlc[i]["close"] <= ohlc[i]["ema50"]:
            break
        analysis["candle_cnt_close_above_ema50"] += 1

    for i in range(n - 1, -1, -1):
        if ohlc[i]["close"] >= ohlc[i]["ema50"]:
            break
        analysis["candle_cnt_close_below_ema50"] += 1

    for i in range(n - 1, -1, -1):
        if ohlc[i]["ema50"] <= ohlc[i]["ema200"]:
            break
        analysis["candle_cnt_ema50_above_ema200"] += 1

    for i in range(n - 1, -1, -1):
        if ohlc[i]["ema50"] >= ohlc[i]["ema200"]:
            break
        analysis["candle_cnt_ema50_below_ema200"] += 1

    if (
        analysis["close_above_emas"]
        and analysis["is_ema20_in_uptrend"]
        and analysis["is_ema50_in_uptrend"]
        and analysis["is_ema200_in_uptrend"]
        and analysis["candle_cnt_close_above_ema50"] >= 5
        and analysis["candle_cnt_ema50_above_ema200"] >= 5
    ):
        analysis["signal"] = kite.TRANSACTION_TYPE_BUY

    if (
        analysis["close_below_emas"]
        and analysis["is_ema20_in_downtrend"]
        and analysis["is_ema50_in_downtrend"]
        and analysis["is_ema200_in_downtrend"]
        and analysis["candle_cnt_close_below_ema50"] >= 5
        and analysis["candle_cnt_ema50_below_ema200"] >= 5
    ):
        analysis["signal"] = kite.TRANSACTION_TYPE_SELL

    return analysis

def _cnt_above_below(left_key: str, right_key: str, ohlc: list):
    cnt = 0
    for i in range(len(ohlc) - 1, -30, -1):
        if ohlc[i][left_key] <= ohlc[i][right_key]:
            break
        cnt += 1
    return cnt

def s8(ohlc: list):
    curr = ohlc[-1]
    analysis = {
        "close_above_emas": curr["close"] > curr["ema20"] > curr["ema50"] > curr["ema200"],
        "close_below_emas": curr["close"] < curr["ema20"] < curr["ema50"] < curr["ema200"],
        **curr,
        "candle_cnt_close_above_ema50": _cnt_above_below("close", "ema50", ohlc),
        "candle_cnt_close_below_ema50": _cnt_above_below("ema50", "close", ohlc),
        "candle_cnt_ema50_above_ema200": _cnt_above_below("ema50", "ema200", ohlc),
        "candle_cnt_ema50_below_ema200": _cnt_above_below("ema200", "ema50", ohlc),
        "signal": None,
        "date": str(curr["date"]),
    }

    if (
        analysis["close_above_emas"]
        and analysis["is_ema20_in_uptrend"]
        and analysis["is_ema50_in_uptrend"]
        and analysis["is_ema200_in_uptrend"]
        and analysis["candle_cnt_close_above_ema50"] >= 5
        and analysis["candle_cnt_ema50_above_ema200"] >= 5
        and analysis["supertrend_dir"] == 1
    ):
        analysis["signal"] = kite.TRANSACTION_TYPE_BUY

    if (
        analysis["close_below_emas"]
        and analysis["is_ema20_in_downtrend"]
        and analysis["is_ema50_in_downtrend"]
        and analysis["is_ema200_in_downtrend"]
        and analysis["candle_cnt_close_below_ema50"] >= 5
        and analysis["candle_cnt_ema50_below_ema200"] >= 5
        and analysis["supertrend_dir"] == -1
    ):
        analysis["signal"] = kite.TRANSACTION_TYPE_SELL

    return analysis