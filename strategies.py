def s1(ohlc):
    curr = ohlc[-1]
    analysis = {
        "close_above_emas": curr["close"]
        > curr["ema20"]
        > curr["ema50"]
        > curr["ema100"]
        > curr["ema200"],
        "close_below_emas": curr["close"]
        < curr["ema20"]
        < curr["ema50"]
        < curr["ema100"]
        < curr["ema200"],
        **curr,
        "signal": None,
    }

    if (
        analysis["close_above_emas"]
        and analysis["ema20_uptrend_time_span"] >= 10
        and analysis["is_ema50_in_uptrend"]
    ):
        analysis["signal"] = "BUY"

    if (
        analysis["close_below_emas"]
        and analysis["ema20_downtrend_time_span"] >= 10
        and analysis["is_ema50_in_downtrend"]
    ):
        analysis["signal"] = "SELL"

    return analysis


def s2(ohlc):
    curr = ohlc[-1]
    analysis = {
        "close_above_emas": curr["close"] > curr["ema50"] > curr["ema200"],
        "close_below_emas": curr["close"] < curr["ema50"] < curr["ema200"],
        **curr,
        "signal": None,
    }

    if (
        analysis["close_above_emas"]
        and analysis["ema50_uptrend_time_span"] >= 10
        and analysis["is_ema20_in_uptrend"]
    ):
        analysis["signal"] = "BUY"

    if (
        analysis["close_below_emas"]
        and analysis["ema50_downtrend_time_span"] >= 10
        and analysis["is_ema20_in_downtrend"]
    ):
        analysis["signal"] = "SELL"

    return analysis


def s3(ohlc):
    curr = ohlc[-1]
    analysis = {
        "close_above_emas": curr["close"]
        > curr["ema20"]
        > curr["ema50"]
        > curr["ema200"],
        "close_below_emas": curr["close"]
        < curr["ema20"]
        < curr["ema50"]
        < curr["ema200"],
        **curr,
        "signal": None,
    }

    if (
        analysis["close_above_emas"]
        and analysis["ema20_uptrend_time_span"] >= 10
        and analysis["ema50_uptrend_time_span"] >= 10
    ):
        analysis["signal"] = "BUY"

    if (
        analysis["close_below_emas"]
        and analysis["ema20_downtrend_time_span"] >= 10
        and analysis["ema50_downtrend_time_span"] >= 10
    ):
        analysis["signal"] = "SELL"

    return analysis


def s4(ohlc):
    curr = ohlc[-1]
    analysis = {
        "close_above_emas": curr["close"] > curr["ema50"] > curr["ema200"],
        "close_below_emas": curr["close"] < curr["ema50"] < curr["ema200"],
        **curr,
        "signal": None,
    }

    if (
        analysis["close_above_emas"]
        and analysis["is_ema50_in_uptrend"]
        and analysis["is_ema200_in_uptrend"]
    ):
        analysis["signal"] = "BUY"

    if (
        analysis["close_below_emas"]
        and analysis["is_ema50_in_downtrend"]
        and analysis["is_ema200_in_downtrend"]
    ):
        analysis["signal"] = "SELL"

    return analysis


def s5(ohlc):
    curr = ohlc[-1]
    analysis = {
        "close_above_emas": curr["close"] > curr["ema50"] > curr["ema200"],
        "close_below_emas": curr["close"] < curr["ema50"] < curr["ema200"],
        **curr,
        "candle_cnt_close_above_ema50": 0,
        "candle_cnt_close_below_ema50": 0,
        "signal": None,
    }

    for i in range(len(ohlc) - 1, -1, -1):
        if ohlc[i]["close"] <= ohlc[i]["ema50"]:
            break
        analysis["candle_cnt_close_above_ema50"] += 1

    for i in range(len(ohlc) - 1, -1, -1):
        if ohlc[i]["close"] >= ohlc[i]["ema50"]:
            break
        analysis["candle_cnt_close_below_ema50"] += 1

    if (
        analysis["close_above_emas"]
        and analysis["is_ema50_in_uptrend"]
        and analysis["is_ema200_in_uptrend"]
        and analysis["candle_cnt_close_above_ema50"] >= 5
    ):
        analysis["signal"] = "BUY"

    if (
        analysis["close_below_emas"]
        and analysis["is_ema50_in_downtrend"]
        and analysis["is_ema200_in_downtrend"]
        and analysis["candle_cnt_close_below_ema50"] >= 5
    ):
        analysis["signal"] = "SELL"

    return analysis


def s6(ohlc):
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
        and analysis["is_ema50_in_uptrend"]
        and analysis["is_ema200_in_uptrend"]
        and analysis["candle_cnt_close_above_ema50"] >= 5
        and analysis["candle_cnt_ema50_above_ema200"] >= 5
    ):
        analysis["signal"] = "BUY"

    if (
        analysis["close_below_emas"]
        and analysis["is_ema50_in_downtrend"]
        and analysis["is_ema200_in_downtrend"]
        and analysis["candle_cnt_close_below_ema50"] >= 5
        and analysis["candle_cnt_ema50_below_ema200"] >= 5
    ):
        analysis["signal"] = "SELL"

    return analysis


def s7(ohlc):
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
        analysis["signal"] = "BUY"

    if (
        analysis["close_below_emas"]
        and analysis["is_ema20_in_downtrend"]
        and analysis["is_ema50_in_downtrend"]
        and analysis["is_ema200_in_downtrend"]
        and analysis["candle_cnt_close_below_ema50"] >= 5
        and analysis["candle_cnt_ema50_below_ema200"] >= 5
    ):
        analysis["signal"] = "SELL"

    return analysis


def s8(ohlc):
    curr, n = ohlc[-1], len(ohlc)
    analysis = {
        "close_above_emas": curr["close"] > curr["ema50"] > curr["ema200"],
        "close_below_emas": curr["close"] < curr["ema50"] < curr["ema200"],
        **curr,
        "candle_cnt_ema20_above_ema50": 0,
        "candle_cnt_ema20_below_ema50": 0,
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
    
    for i in range(n - 1, -1, -1):
        if ohlc[i]["ema20"] <= ohlc[i]["ema50"]:
            break
        analysis["candle_cnt_ema20_above_ema50"] += 1
    
    for i in range(n - 1, -1, -1):
        if ohlc[i]["ema20"] >= ohlc[i]["ema50"]:
            break
        analysis["candle_cnt_ema20_below_ema50"] += 1
        

    if (
        analysis["close_above_emas"]
        and analysis["is_ema5_in_uptrend"]
        and analysis["is_ema20_in_uptrend"]
        and analysis["is_ema50_in_uptrend"]
        and analysis["is_ema200_in_uptrend"]
        and analysis["candle_cnt_close_above_ema50"] >= 5
        and analysis["candle_cnt_ema50_above_ema200"] >= 5
        and analysis["candle_cnt_ema20_above_ema50"] >= 5
    ):
        analysis["signal"] = "BUY"

    if (
        analysis["close_below_emas"]
        and analysis["is_ema5_in_downtrend"]
        and analysis["is_ema20_in_downtrend"]
        and analysis["is_ema50_in_downtrend"]
        and analysis["is_ema200_in_downtrend"]
        and analysis["candle_cnt_close_below_ema50"] >= 5
        and analysis["candle_cnt_ema50_below_ema200"] >= 5
        and analysis["candle_cnt_ema20_below_ema50"] >= 5
    ):
        analysis["signal"] = "SELL"

    return analysis

def s9(ohlc):
    curr, n = ohlc[-1], len(ohlc)
    analysis = {
        "close_above_emas": curr["close"] > curr["ema50"] > curr["ema200"],
        "close_below_emas": curr["close"] < curr["ema50"] < curr["ema200"],
        **curr,
        "candle_cnt_ema20_above_ema50": 0,
        "candle_cnt_ema20_below_ema50": 0,
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
    
    for i in range(n - 1, -1, -1):
        if ohlc[i]["ema20"] <= ohlc[i]["ema50"]:
            break
        analysis["candle_cnt_ema20_above_ema50"] += 1
    
    for i in range(n - 1, -1, -1):
        if ohlc[i]["ema20"] >= ohlc[i]["ema50"]:
            break
        analysis["candle_cnt_ema20_below_ema50"] += 1
        

    if (
        analysis["close_above_emas"]
        and analysis["is_ema20_in_uptrend"]
        and analysis["is_ema50_in_uptrend"]
        and analysis["is_ema200_in_uptrend"]
        and analysis["candle_cnt_close_above_ema50"] >= 5
        and analysis["candle_cnt_ema50_above_ema200"] >= 5
        and analysis["candle_cnt_ema20_above_ema50"] >= 5
    ):
        analysis["signal"] = "BUY"

    if (
        analysis["close_below_emas"]
        and analysis["is_ema20_in_downtrend"]
        and analysis["is_ema50_in_downtrend"]
        and analysis["is_ema200_in_downtrend"]
        and analysis["candle_cnt_close_below_ema50"] >= 5
        and analysis["candle_cnt_ema50_below_ema200"] >= 5
        and analysis["candle_cnt_ema20_below_ema50"] >= 5
    ):
        analysis["signal"] = "SELL"

    return analysis