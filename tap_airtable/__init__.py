from singer import utils
from tap_airtable.services import Airtable


REQUIRED_CONFIG_KEYS = [
    'metadata_url',
    'records_url',
    'token',
    'base_id',
    'selected_by_default'
]


def main():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    if args.discover:
        Airtable.run_discovery(args)
    elif args.properties:
        Airtable.run_sync(args.config, args.properties)


if __name__ == "__main__":
    main()
