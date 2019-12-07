import json
from tap_airtable.services import Airtable


with open('./../config.json', 'r') as f:
    config = json.load(f)
    base_id = config["base_id"]

Airtable.run_discovery(base_id)

Airtable.run_tap(base_id)
