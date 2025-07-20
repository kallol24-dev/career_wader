import json
import os

CITY_CODES_PATH = os.path.join(os.path.dirname(__file__), 'city_codes.json')

with open(CITY_CODES_PATH, 'r') as f:
    CITY_CODES = json.load(f)