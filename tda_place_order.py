#!/usr/bin/env python3

from secrets import TDA_ACCOUNT_ID
from lib import tda_login, validate_tickers_basic_regex
from tda.orders.equities import equity_buy_limit, equity_sell_limit
from tda.orders.common import Duration, Session, Destination
import sys
import json
import httpx

if (len(sys.argv) != 3) or (sys.argv[1].lower() not in {"buy", "sell"}):
    print(json.dumps({"error": "Expected exactly two arguments. Usage: `<buy/sell> <ticker>`"}))
    sys.exit(1)

# Go ahead and do this validation even though we check exact equities below
target_ticker = validate_tickers_basic_regex([sys.argv[2]])[0].upper()
action = sys.argv[1].lower()

allowed_equities = {
        # No forex on TDA for now
        #"ZAR/JPY", "HKD/JPY",
        "HIVE"}

if target_ticker not in allowed_equities:
    print(f'{{"error": "{target_ticker} is not an allowed equity! Allowed equities: {allowed_equities}"}}')
    sys.exit(1)

c = tda_login()

quote_resp = c.get_quotes([target_ticker])

if not quote_resp.is_success:
    quote_resp.raise_for_status()

quote_data = quote_resp.json()

if action == "buy":
    bid_ask = "bid"
    quote = quote_data[target_ticker]
    price = quote.get('bidPrice') or quote.get("bidPriceInDouble")
    duration = Duration.GOOD_TILL_CANCEL
    order = (equity_buy_limit(target_ticker, 1, price)
        .set_duration(duration)
        .set_session(Session.SEAMLESS)
        .build())
else:
    bid_ask = "ask"
    quote = quote_data[target_ticker]
    price = quote.get('askPrice') or quote.get("askPriceInDouble")
    duration = Duration.GOOD_TILL_CANCEL
    order = (equity_sell_limit(target_ticker, 1, price)
        .set_duration(duration)
        .set_session(Session.SEAMLESS)
        .build())

try:
    r = c.place_order(TDA_ACCOUNT_ID, order)
    r.raise_for_status()
except httpx.HTTPStatusError as exc:
    print(json.dumps({"error": f"Failed response from TDA API: {exc.response.status_code}: {exc}"}))
else:
    print(json.dumps({"success": f"Successfully placed a LIMIT order to {action} 1 unit of {target_ticker} at the current {bid_ask} price of {price} with {duration}."}))
