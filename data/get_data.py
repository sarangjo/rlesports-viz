import copy
import json
import re
import sys
from typing import List, Any, Dict
import time

import requests

from api import call_api
from tournaments import get_tournaments_data, process_tournaments_data


def main():
    output = get_tournaments_data()
    process_tournaments_data(output)


if __name__ == '__main__':
    main()
