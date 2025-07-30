import json
from pathlib import Path

WORKING_DIR = function_path = str(Path(__file__).resolve().parents[0])
countries = json.load(open(f'{WORKING_DIR}/country.json'))


def get_country_name(country_code):
    return countries.get(country_code, None)
