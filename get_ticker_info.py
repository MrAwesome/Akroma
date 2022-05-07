#!/usr/bin/env python3

from robin_stocks import robinhood as r
from pprint import pprint
from typing import List, Dict
import time
import regex
import json

login_data = r.login()

tickers = open("./tickers.txt").read().strip().split('\n')

#pricebook = r.stocks.get_pricebook_by_symbol(ticker)
#quote = r.stocks.get_stock_quote_by_symbol(ticker)
#historicals = r.stocks.get_stock_historicals(ticker)
#instruments = r.stocks.get_instruments_by_symbols(ticker)

def maybe_to_float(x: any):
    if isinstance(x, str):
        if regex.match(r'^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$', x):
            return float(x)
    return x

ticker_to_exp_dates_to_info: Dict[str, Dict[str, any]] = {}
all_info = []

for ticker in tickers:
    chains = r.options.get_chains(ticker)
    expiration_dates: List[str] = chains['expiration_dates']
    from_year = [x for x in expiration_dates if x.startswith('2022')]
    from_year.sort()
    last_date = from_year[-1]
    exp_dates = [last_date]
    ticker_to_exp_dates_to_info[ticker] = {exp_date: {} for exp_date in exp_dates}

timestamp = str(int(time.time()))
for (ticker, exp_dates) in ticker_to_exp_dates_to_info.items():
    for exp_date in exp_dates:
        parsed_infolist = []
        infolist = r.options.find_options_by_expiration(ticker, exp_date, optionType='put')
        #ticker_to_exp_dates_to_info[ticker][exp_date] = infolist
        for info in infolist:
            parsed_info = { k: maybe_to_float(v) for (k, v) in info.items() }
            #parsed_info['_time'] = timestamp
            parsed_infolist.append(parsed_info)
            all_info.append(parsed_info)

