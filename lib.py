from secrets import TDA_CLIENT_ID
from tda import auth, client
from pprint import pprint
from typing import List
import sys
import json
import regex

TOK_PATH = 'tda_token.json'
API_KEY = f'{TDA_CLIENT_ID}@AMER.OAUTHAP'
REDIRECT_URI = 'http://localhost'
ALL_FOREX_PAIRS = ["AUD/CAD", "AUD/CHF", "AUD/JPY", "AUD/NOK", "AUD/NZD", "AUD/PLN", "AUD/SGD", "AUD/USD", "CAD/CHF", "CAD/JPY", "CAD/NOK", "CAD/PLN", "CHF/HUF", "CHF/JPY", "CHF/NOK", "CHF/PLN", "EUR/AUD", "EUR/CAD", "EUR/CHF", "EUR/CZK", "EUR/DKK", "EUR/GBP", "EUR/HKD", "EUR/HUF", "EUR/JPY", "EUR/MXN", "EUR/NOK", "EUR/NZD", "EUR/PLN", "EUR/SEK", "EUR/SGD", "EUR/USD", "EUR/ZAR", "GBP/AUD", "GBP/CAD", "GBP/CHF", "GBP/DKK", "GBP/HKD", "GBP/JPY", "GBP/NOK", "GBP/NZD", "GBP/PLN", "GBP/SEK", "GBP/SGD", "GBP/USD", "GBP/ZAR", "HKD/JPY", "NOK/JPY", "NOK/SEK", "NZD/CAD", "NZD/CHF", "NZD/JPY", "NZD/USD", "SGD/HKD", "SGD/JPY", "USD/CAD", "USD/CHF", "USD/CZK", "USD/DKK", "USD/HKD", "USD/HUF", "USD/ILS", "USD/JPY", "USD/MXN", "USD/NOK", "USD/PLN", "USD/SEK", "USD/SGD", "USD/ZAR", "ZAR/JPY"]

def tda_login():
    try:
        c = auth.client_from_token_file(TOK_PATH, API_KEY)
    except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Chrome() as driver:
            c = auth.client_from_login_flow(driver, API_KEY, REDIRECT_URI, TOK_PATH)
    return c

def tda_extract_json(response):
    if (response[1] is not None):
        raise response[1]
    else:
        text = response[0].text
        parsed = json.loads(text)
        return parsed

def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])

def validate_tickers_basic_regex(tokens: List[str]) -> List[str]:
    invalid_tokens = []
    for tok in tokens:
        if not regex.match(r'^[a-zA-Z/]+$', tok):
            invalid_tokens.append(tok)

    if invalid_tokens:
        print('{"error": "Invalid tickers: '+str(invalid_tokens)+'"}')
        sys.exit(1)

    return tokens

# Helper function for finding TDA_ACCOUNT_ID. Run this file with `python -i lib.py`A and then run this function to see your account info.
def tda_get_accounts_info():
    c = tda_login()
    accounts_info = c.get_accounts().json()
    pprint(accounts_info)
