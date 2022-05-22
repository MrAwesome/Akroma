#!/usr/bin/env python3

# TODO: enable asyncio

from lib import tda_login, validate_tickers_basic_regex
import json
import sys
import httpx

if len(sys.argv) < 2:
    print('{"error": "Expected at least one argument."}')
    sys.exit(1)

tokens = validate_tickers_basic_regex(sys.argv[1:])
c = tda_login()

try:
    r = c.get_quotes(tokens)
    r.raise_for_status()
except httpx.HTTPStatusError as exc:
    print(json.dumps({"error": f"Failed response from TDA API: {exc.response.status_code}: {exc}"}))
else:
    print(f'{{"success": {r.text} }}')
