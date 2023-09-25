from singer import utils
from tap_airtable.services import Airtable


REQUIRED_CONFIG_KEYS = [
    'metadata_url',
    'records_url',
    'client_id',
    'client_secret',
    'access_token',
    'refresh_token',
    'base_id',
    'selected_by_default',
    'remove_emojis'
]


def main():
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    airtable = Airtable()
    if args.discover:
        airtable.run_discovery(args)
    elif args.properties:
        airtable.run_sync(args.config, args.properties)


if __name__ == "__main__":
    main()
