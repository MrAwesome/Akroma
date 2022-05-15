#!/usr/bin/env python3

from lib import tda_login, validate_tickers_basic_regex
import sys

if (len(sys.argv) != 3) or (sys.argv[1] not in {"buy", "sell"}):
    print('{"error": "Expected exactly two arguments. Usage: `<buy/sell> <ticker>`"}')
    sys.exit(1)

# Go ahead and do this validation even though we check exact equities below
target_ticker = validate_tickers_basic_regex([sys.argv[2]])[0].upper()

allowed_equities = {"ZAR/JPY"}

if target_ticker not in allowed_equities:
    print(f'{{"error": "{target_ticker} is not an allowed equity! Allowed equities: {allowed_equities}"}}')
    sys.exit(1)

c = tda_login()

c.place_order

print("will perform a buy/sell here")
