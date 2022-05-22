#!/usr/bin/env python3

import json
from lib import tda_login, TOK_PATH

error = None
try:
    c = tda_login()
    c.ensure_updated_refresh_token()
    has_token = True
except Exception as e:
    has_token = False
    error = e

if has_token:
    ret = {
        "success": True,
        "tokenPath": TOK_PATH,
    }
else:
    ret = {
        "success": False,
        "error": error
    }

print(json.dumps(ret))
