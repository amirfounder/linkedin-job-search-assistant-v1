from __future__ import annotations

import json
from json import JSONEncoder
from os.path import isfile


comparator_map = {
    'EQ': lambda obj_value, filter_value: obj_value == filter_value,
    'NEQ': lambda obj_value, filter_value: obj_value != filter_value,
    'LT': lambda obj_value, filter_value: obj_value < filter_value,
    'LTE': lambda obj_value, filter_value: obj_value <= filter_value,
    'GT': lambda obj_value, filter_value: obj_value > filter_value,
    'GTE': lambda obj_value, filter_value: obj_value >= filter_value,
}


class RecruiterEncoder(JSONEncoder):
    def default(self, o: Recruiter) -> dict:
        return o.to_dict()


class Recruiter:
    keys = [
        'name',
        'url',
        'company',
        'sent_connection_invite',
        'sent_connection_invite_follow_up',
        'last_contacted',
    ]
    key_set = set(keys)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.key_set:
                setattr(self, k, v)

    @classmethod
    def from_dict(cls, params):
        return cls(**params)

    def to_dict(self):
        return {k: getattr(self, k, None) for k in self.keys}


def create_file(path):
    if not isfile(path):
        open(path, 'x').close()


class CMS:
    def __init__(self):
        self.path = 'data/cms.json'
        self.header = Recruiter.keys
        self.recruiters = []
        create_file(self.path)

    def load(self):
        with open(self.path, 'r') as f:
            try:
                self.recruiters.extend([Recruiter(**obj) for obj in json.loads(f.read())])
            except Exception as e:
                print(f'Suppressing {type(e).__name__} exception: {str(e)}')

    def flush(self):
        with open(self.path, 'w') as f:
            f.write(json.dumps(self.recruiters, cls=RecruiterEncoder))

    def add(self, recruiter: Recruiter):
        self.recruiters.append(recruiter)
        self.flush()

    def query(self, params: dict):
        for recruiter in self.recruiters:

            is_valid = True
            for key, filterable in params.items():

                if not hasattr(recruiter, key):
                    continue

                if isinstance(filterable, dict):
                    comparator, filter_value = filterable['comparator'], filterable['value']
                else:
                    comparator, filter_value = 'EQ', filterable

                comparator_fn = comparator_map[comparator]
                obj_value = getattr(recruiter, key)

                if not comparator_fn(obj_value, filter_value):
                    is_valid = False
                    break

            if is_valid:
                yield recruiter
