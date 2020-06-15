import sys
import requests
import json
from typing import Dict, Any

API_BASE = "https://liquipedia.net/rocketleague/api.php"
DEFAULT_PARAMS = {"origin": "*", "format": "json"}


def call_api(opts: Dict[str, Any]):
    opts.update(DEFAULT_PARAMS)
    req = requests.get(API_BASE, opts)
    try:
        return json.loads(req.text)
    except json.decoder.JSONDecodeError:
        print(req.text)
        sys.exit(1)
