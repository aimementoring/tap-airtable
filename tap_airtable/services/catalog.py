import json
import sys


class CatalogEntry:

    def __init__(self, base):
        self.name = base['name']
        self.properties = base['properties']

    def __repr__(self):
        return self.__dict__

    def __str__(self):
        return json.dumps(self.__dict__)

    def to_dict(self):
        result = {}

        if self.name:
            result['name'] = self.name
        if self.properties:
            result['properties'] = self.properties

        return result


class Catalog:

    def __init__(self, streams):
        self.streams = streams

    def __str__(self):
        return json.dumps(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_dict(self):
        return [stream.to_dict() for stream in self.streams]

    def dump(self):
        json.dump(self.to_dict(), sys.stdout, indent=2)
