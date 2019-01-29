import random, string


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
