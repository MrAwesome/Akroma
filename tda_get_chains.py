# NOTE: requires a `pip install tda-api`
from tda import client

from lib import flatten, tda_login
from pprint import pprint
import json
import sys
import regex
import time

if len(sys.argv) < 2:
    print('{"error": "Expected at least one argument."}')
    sys.exit()

tokens = sys.argv[1:]

invalid_tokens = []
for tok in tokens:
    if not regex.match(r'^[a-zA-Z/]+$', tok):
        invalid_tokens.append(tok)

if invalid_tokens:
    print('{"error": "Invalid tickers: '+str(invalid_tokens)+'"}')
    sys.exit()

c = tda_login()

fullchains = {}
objs = []
failed = []

for ticker in tokens:
    r = c.get_option_chain(ticker, contract_type=client.Client.Options.ContractType.PUT, strike_range=client.Client.Options.StrikeRange.OUT_OF_THE_MONEY,)
    if r.status_code != 200:
        failed.append(r)
        continue
    respjson = r.json()
    fullchains[ticker] = respjson
    onlydateswelike = {x: y for (x, y) in respjson['putExpDateMap'].items() if (x.startswith('2022-05') or x.startswith('2022-06'))}

    for date, striketoinfo in onlydateswelike.items():
        for strikeprice, info in striketoinfo.items():
            for x in info:
                if x['inTheMoney'] is False:
                    objs.append(x)

    #time.sleep(0.1)

print(json.dumps(objs))

#for x, y in [(x['symbol'], x['ask']) for x in objs if x['ask'] < 0.05]:
#    print(y, x)
