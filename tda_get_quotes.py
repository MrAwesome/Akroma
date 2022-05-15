#!/usr/bin/env python3

# TODO: enable asyncio

from lib import tda_login, validate_tickers_basic_regex
import sys

if len(sys.argv) < 2:
    print('{"error": "Expected at least one argument."}')
    sys.exit(1)

tokens = validate_tickers_basic_regex(sys.argv[1:])
c = tda_login()

r = c.get_quotes(tokens)
if r.status_code != 200:
    r.raise_for_status()
print(r.text)
