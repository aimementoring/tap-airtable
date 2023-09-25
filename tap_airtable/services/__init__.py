import json
import uuid
import backoff
import singer
import requests

from airtable.client import Client
from singer.catalog import Catalog, CatalogEntry, Schema
from tap_airtable.airtable_utils import JsonUtils, Relations

class Airtable(object):
    with open('./config.json', 'r') as f:
        config = json.load(f)
        client = Client(
            config["client_id"],
            config["client_secret"],
            config["redirect_uri"],
            uuid.uuid4().__str__().replace("-", "")*2
        )
        metadata_url = config["metadata_url"]
        records_url = config["records_url"]
        token = config["access_token"]
        refresh_token = config["refresh_token"]

    def _gen_new_token_url(self):
        url = self.client.authorization_url(uuid.uuid4().__str__().replace("-", ""))
        print(url)
    
    def gen_new_token(self, code):
        response = self.client.token_creation(code)
        self.token = response["access_token"]
        self.refresh_token = response["refresh_token"]
        self.config["access_token"] = response["access_token"]
        self.config["refresh_token"] = response["refresh_token"]
        with open('./config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def _refresh_token(self):
        """Refresh OAuth token."""
        self.client.set_token({
            "access_token": self.token,
            "refresh_token": self.refresh_token,
        })
        response = self.client.refresh_token(self.refresh_token)
        self.token, self.config["access_token"] = response["access_token"], response["access_token"]
        with open('./config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def validate_response(self, response: requests.Response) -> None:
        """Validate HTTP response."""
        if response.status_code == 401:
            self._refresh_token()
        
        if response.status_code == 429:
            raise Exception(f"Too Many Requests for path: {response.request.url}")
        
        if response.status_code == 404:
            pass
        elif 400 <= response.status_code < 500:
            msg = (
                f"{response.status_code} Client Error: "
                f"{response.reason} for path: {response.request.url}"
                f" with text:{response.text} "
            )
            raise Exception(msg)

        elif 500 <= response.status_code < 600:
            msg = (
                f"{response.status_code} Server Error: "
                f"{response.reason} for path: {response.request.url}"
                f" with text:{response.text} "
            )
            raise Exception(msg)

        return response
    
    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
    def _request(self, method, url, params=None, headers={}, data={}, *args, **kwargs):
        new_headers = {'Authorization': 'Bearer {}'.format(self.config['access_token'])}
        headers.update(new_headers)
        response = requests.request(method, url, params=params, headers=headers, data=data, *args, **kwargs)
        return self.validate_response(response)

    def run_discovery(self, args):
        response = self._request(method = 'GET', url=args.config['metadata_url'] + "bases/" + args.config['base_id'] + "/tables")
        entries = []

        for table in response.json()["tables"]:

            columns = {}
            table_name = table["name"]

            # Create schema
            base = {
                "type": "object",
                "additionalProperties": False,
                "properties": columns
            }

            # Create metadata
            metadata = [{
                "breadcrumb": [],
                "metadata": {
                    "inclusion": "available"
                }
            }]

            columns["id"] = {"type": ["null", "string"], 'key': True}

            for field in table["fields"]:
                if not field["name"] == "Id":
                    columns[field["name"]] = {"type": ["null", "string"]}

                metadata.append({
                    'metadata': {
                        'inclusion': 'available'
                    },
                    'breadcrumb': ['properties', field["name"]]
                })

            schema = Schema.from_dict(base)

            entry = CatalogEntry(
                table=table_name,
                stream=table_name,
                schema=schema,
                metadata=metadata)
            entries.append(entry)

        return Catalog(entries).dump()

    def is_selected(metadata):
        mdata = singer.metadata.to_map(metadata)
        root_metadata = mdata.get(())
        return root_metadata and root_metadata.get('selected') is True

    @classmethod
    def run_sync(cls, config, properties):

        streams = properties['streams']
        airtable_instance = Airtable()

        for stream in streams:
            table = stream['table_name'].replace('/', '')
            table = table.replace(' ', '')
            table = table.replace('{', '')
            table = table.replace('}', '')
            schema = stream['schema']
            metadata = stream['metadata']

            if table != 'relations' and cls.is_selected(metadata):
                response = airtable_instance.get_response(config['base_id'], stream["table_name"])
                if response.json().get('records'):
                    records = JsonUtils.match_record_with_keys(schema,
                                                               response.json().get('records'),
                                                               config['remove_emojis'])

                    singer.write_schema(table, schema, 'id')
                    singer.write_records(table, records)

                    offset = response.json().get("offset")

                    while offset:
                        response = airtable_instance.get_response(config['base_id'], stream["table_name"], offset)
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

    def get_response(cls, base_id, table, offset=None):
        table = table.replace('/', '%2F')

        if offset:
            request = cls.records_url + base_id + '/' + table + '?offset={}'.format(offset)
        else:
            request = cls.records_url + base_id + '/' + table

        return cls._request(method='GET', url=request)
