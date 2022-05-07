#!/usr/bin/env python3

# NOTE: requires a `pip install tda-api`

from pprint import pprint

from lib import flatten, tda_login
import json
import sys
import regex

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

#r = c.get_price_history('SPY',
        #period_type=client.Client.PriceHistory.PeriodType.MONTH,
        #period=client.Client.PriceHistory.Period.ONE_MONTH,
        #frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
        #frequency=client.Client.PriceHistory.Frequency.DAILY)
#r = c.get_option_chain('SPY',
        #contract_type=client.Client.Options.ContractType.PUT,
        #strike_range=client.Client.Options.StrikeRange.OUT_OF_THE_MONEY,
        #)
r = c.get_quotes(tokens)
assert r.status_code == 200, r.raise_for_status()
print(r.json())

#lawl = open('/tmp/lawl.json', 'w')
#muh_datemap = chain['putExpDateMap']
#out = [data[0] for (exp_date, by_strike) in muh_datemap.items() for (strike_price, data) in by_strike.items()]
#flat = flatten(out)

#parsed = []
#for x in flat:
    #expDate = x["expirationDate"]
    #x["expirationDate"] = print(datetime.fromtimestamp(t).isoformat())

