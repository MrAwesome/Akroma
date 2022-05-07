#!/usr/bin/env python3

from robin_stocks import robinhood as r
from pprint import pprint
import time

r.login()

etf_tickers = open("./tickers.txt").read().strip().split('\n')
seen_ids = set()
original_etf_tickers = set(etf_tickers)
known_etfs = {}
new_etfs = {}
new_stocks = {}

# Returns whether or not the target equity is an ETF.
def get_holdings(muh_holding_id: str, muh_ticker: str) -> bool:
    if muh_holding_id is None:
        return
    if muh_holding_id in seen_ids:
        return

    seen_ids.add(muh_holding_id)

    etf_instrument_url = f'https://bonfire.robinhood.com/instruments/{muh_holding_id}/etp-details/'
    maybe_etf_instrument = r.request_get(etf_instrument_url)

    if maybe_etf_instrument is not None:
        known_etfs[muh_ticker] = maybe_etf_instrument
        if muh_ticker not in original_etf_tickers:
            new_etfs[muh_ticker] = maybe_etf_instrument
        holdings = maybe_etf_instrument['holdings']
        if holdings:
            for h in holdings:
                instrument_id = h['instrument_id']
                ticker = h['symbol']
                if not get_holdings(instrument_id, ticker):
                    new_stocks[ticker] = h

                time.sleep(1)
            return True
    #else:
        #seen_tickers_stocks.add(muh_ticker)
    return False

for etf_ticker in etf_tickers:
    etf_id = r.stocks.id_for_stock(etf_ticker)
    get_holdings(etf_id, etf_ticker)
