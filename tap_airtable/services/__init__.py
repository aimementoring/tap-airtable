from tap_airtable.airtable_utils import JsonUtils, Relations
import requests
import singer
from singer.catalog import Catalog, CatalogEntry


class Airtable():

    def __init__(self, config):
        self.config = config
        self.metadata_url = self.config["metadata_url"]
        self.records_url = self.config["records_url"]
        self.token = self.config["token"]

    def run_discovery(self, args):
        headers = {'Authorization': 'Bearer {}'.format(args.config['token'])}
        response = requests.get(url=args.config['metadata_url'] + args.config['base_id'], headers=headers)
        entries = []

        for table in response.json()["tables"]:

            columns = {}
            table_name = table["name"]
            base = {"selected": args.config['selected_by_default'],
                    "name": table_name,
                    "properties": columns}

            columns["record_id"] = {"type": ["null", "string"], 'key': True}

            for field in table["fields"]:
                if not field["name"] == "Id":
                    columns[field["name"]] = {"type": ["null", "string"]}

            entry = CatalogEntry(
                table=table_name,
                stream=table_name,
                metadata=base)
            entries.append(entry)

        return Catalog(entries).dump()

    def run_sync(self, config, properties):

        streams = properties['streams']

        for stream in streams:
            table = stream['table_name'].replace('/', '')
            table = table.replace(' ', '')
            table = table.replace('{', '')
            table = table.replace('}', '')
            schema = stream['metadata']

            if table != 'relations' and schema['selected']:
                response = self.get_response(config['base_id'], schema["name"])
                if response.json().get('records'):
                    records = JsonUtils.match_record_with_keys(schema,
                                                               response.json().get('records'),
                                                               config['remove_emojis'])

                    singer.write_schema(table, schema, 'record_id')
                    singer.write_records(table, records)

                    offset = response.json().get("offset")

                    while offset:
                        response = self.get_response(config['base_id'], schema["name"], offset)
                        if response.json().get('records'):
                            records = JsonUtils.match_record_with_keys(schema,
                                                                       response.json().get('records'),
                                                                       config['remove_emojis'])

                        singer.write_records(table, records)
                        offset = response.json().get("offset")

        relations_table = {"name": "relations",
                           "properties": {"id": {"type": ["null", "string"]},
                                          "relation1": {"type": ["null", "string"]},
                                          "relation2": {"type": ["null", "string"]}}}

        singer.write_schema('relations', relations_table, 'id')
        singer.write_records('relations', Relations.get_records())

    def get_response(self, base_id, table, offset=None):

        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        table = table.replace('/', '%2F')

        if offset:
            request = self.records_url + base_id + '/' + table + '?offset={}'.format(offset)
        else:
            request = self.records_url + base_id + '/' + table

        return requests.get(url=request, headers=headers)
