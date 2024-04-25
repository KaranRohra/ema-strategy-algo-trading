from constants import *
from datetime import datetime
from config import *
from strategy.strategy import *


def enter():
    holdings = {}
    holdings[HOLDING_SYMBOL] = SYMBOL
    holdings[HOLDING_ENTRY_DATETIME] = datetime.now()
    holdings[HOLDING_STOPLOSS] = get_stoploss()

    entry_status = None
    scanning_result = get_scanning_result()

    if scanning_result["is_close_gt_ema"] and scanning_result["is_in_uptrend"]:
        holdings[HOLDING_ENTRY_PRICE] = get_entry(dhan.BUY)
        holdings[HOLDING_TRANSACTION_TYPE] = dhan.BUY

        entry_status = "Long Position Entered."
    elif scanning_result["is_close_lt_ema"] and scanning_result["is_in_downtrend"]:
        holdings[HOLDING_ENTRY_PRICE] = get_entry(dhan.SELL)
        holdings[HOLDING_TRANSACTION_TYPE] = dhan.SELL

        entry_status = "Short Position Entered."

    if entry_status:
        pd.DataFrame(data=[holdings]).to_csv(HOLDINGS_CSV_PATH, index=False)

    scanning_result["status"] = entry_status
    return scanning_result


def exit():
    holdings = pd.read_csv(HOLDINGS_CSV_PATH).to_dict(orient="records")[0]
    exit_details = {}
    exit_details[TRADE_SYMBOL] = SYMBOL
    exit_details[TRADE_FROM] = holdings[HOLDING_ENTRY_DATETIME]
    exit_details[TRADE_TO] = datetime.now()
    exit_details[TRADE_ENTRY_PRICE] = holdings[HOLDING_ENTRY_PRICE]
    exit_details[TRADE_EXIT_PRICE] = get_ltp()
    exit_details[TRADE_STOPLOSS] = holdings[HOLDING_STOPLOSS]
    exit_details[TRADE_TRANSACTION_TYPE] = holdings[HOLDING_TRANSACTION_TYPE]

    columns = [
        HOLDING_SYMBOL,
        HOLDING_ENTRY_DATETIME,
        HOLDING_ENTRY_PRICE,
        HOLDING_TRANSACTION_TYPE,
        HOLDING_STOPLOSS,
    ]

    trades_df = pd.read_csv(TRADES_CSV_PATH)
    exit_status = None

    if holdings[HOLDING_TRANSACTION_TYPE] == dhan.BUY and is_close_crossed_ema200(
        dir="lt"
    ):
        exit_details[TRADE_P_AND_L] = (
            exit_details[TRADE_EXIT_PRICE] - exit_details[TRADE_ENTRY_PRICE]
        )
        exit_status = True

    elif holdings[HOLDING_TRANSACTION_TYPE] == dhan.SELL and is_close_crossed_ema200(
        dir="gt"
    ):
        exit_details[TRADE_P_AND_L] = (
            exit_details[TRADE_ENTRY_PRICE] - exit_details[TRADE_EXIT_PRICE]
        )
        exit_status = True

    if exit_status:
        pd.concat(
            [trades_df, pd.DataFrame(data=[exit_details])], ignore_index=True
        ).reset_index().to_csv(TRADES_CSV_PATH, index=False)
        pd.DataFrame(data=[], columns=columns).to_csv(HOLDINGS_CSV_PATH, index=False)
