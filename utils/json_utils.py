from utils.relations_records import Relations


class JsonUtils(object):

    @classmethod
    def match_record_with_keys(cls, schema, records):

        records_to_dump = []

        if records is None:
            return records_to_dump

        for record in records:
            record_to_dump = {}
            id = record.get('id')

            for key in schema.get('properties').keys():
                if not record.get('fields').get(key):
                    record_to_dump[key] = None
                else:
                    if schema['properties'][key]['type'] == ["null", "string"] \
                            or schema['properties'][key]['type'] == ["null", "number"]:
                        record_to_dump[key] = str(record.get('fields').get(key))
                    else:
                        record_to_dump[key] = record.get('fields').get(key)

                Relations.save_if_list_of_ids(record.get('fields').get(key), id)

            record_to_dump['id'] = record.get('id')

            records_to_dump.append(record_to_dump)

        return records_to_dump
