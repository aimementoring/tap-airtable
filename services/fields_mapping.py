import json


class FieldsMapping(object):

    with open('./services/types.json', 'r') as f:
        field_types = json.load(f)

    @classmethod
    def map_field(cls, config):

        primary_type = config["type"]

        if primary_type == "formula":
            return cls.field_types[config["options"]["resultConfig"]["type"]]

        return cls.field_types[primary_type]
