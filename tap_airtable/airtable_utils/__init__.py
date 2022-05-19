import random
import string
import re


class JsonUtils(object):

    @classmethod
    def remove_emojis(cls, record):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)

        return emoji_pattern.sub(r'', record)

    @classmethod
    def match_record_with_keys(cls, schema, records, remove_emojis):

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
                        if remove_emojis:
                            record_to_dump[key] = JsonUtils.remove_emojis(str(record.get('fields').get(key)))
                        else:
                            record_to_dump[key] = str(record.get('fields').get(key))
                    else:
                        if remove_emojis:
                            record_to_dump[key] = JsonUtils.remove_emojis(record.get('fields').get(key))
                        else:
                            record_to_dump[key] = record.get('fields').get(key)

                Relations.save_if_list_of_ids(record.get('fields').get(key), id)

            record_to_dump['record_id'] = record.get('id')

            records_to_dump.append(record_to_dump)

        return records_to_dump


class Relations(object):
    records = []

    @classmethod
    def save_if_list_of_ids(cls, record, id):
        if isinstance(record, list):
            cls.serialize_list_of_ids(record, id)

    @classmethod
    def serialize_list_of_ids(cls, record, id):
        for rec in record:
            record_to_save = {}
            if cls.is_rec_id(rec):
                record_to_save['id'] = cls.random_word(12)
                record_to_save['relation1'] = id
                record_to_save['relation2'] = rec
                cls.records.append(record_to_save)
            else:
                return

    @classmethod
    def is_rec_id(cls, rec):
        if isinstance(rec, str):
            return rec.startswith("rec")
        else:
            return False

    @classmethod
    def get_records(cls):
        return cls.records

    @classmethod
    def random_word(cls, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
