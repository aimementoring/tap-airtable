import json
from singer import utils
from tap_airtable.services import Airtable

REQUIRED_CONFIG_KEYS = [
    'metadata_url',
    'records_url',
    'token',
    'base_id'
]


def main():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    if args.discover:
        Airtable.run_discovery(args)

    #Airtable.run_tap(base_id)


if __name__ == "__main__":
    main()
