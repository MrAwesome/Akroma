from secrets import TDA_CLIENT_ID
from tda import auth, client
import json

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

def tda_login():
    tok_path = 'tda_token.json'
    api_key = f'{TDA_CLIENT_ID}@AMER.OAUTHAP'
    redirect_uri = 'http://localhost'
    try:
        c = auth.client_from_token_file(tok_path, api_key)
    except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Chrome() as driver:
            c = auth.client_from_login_flow(
                driver, api_key, redirect_uri, tok_path)

    return c
