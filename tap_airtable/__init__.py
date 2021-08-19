from singer import utils
from tap_airtable.services import Airtable

REQUIRED_CONFIG_KEYS = [
    'metadata_url',
    'records_url',
    'token',
    'base_id',
    'selected_by_default',
    'remove_emojis'
]


def main():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    airtable = Airtable(args.config)

    if args.discover:
        airtable.run_discovery(args)
    elif args.properties:
        airtable.run_sync(args.config, args.properties)


if __name__ == "__main__":
    main()
