from flatten_dict import flatten
import json
from redis import Redis
from redis.commands.search.field import TextField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search import Search
from redis.exceptions import ResponseError

from chaiverse.database.inferno_database_adapter import _InfernoDatabaseAdapter


class _RedisDatabase(_InfernoDatabaseAdapter):
    def __init__(self, url: str, port: int, password: str):
        self.url = url
        self.port = port
        self.password = password
        self.client = Redis(
            url, port=port, username="default", password=password, decode_responses=True
        )

    def set(self, path: str, value: dict):
        self._set_key(path, value)

    def get(self, path: str, shallow: bool = False):
        records = {}
        path = _clean_key(path)
        for key in self.client.scan_iter(f"{path}*"):
            value = True if shallow else self._get_key(key)
            leaf_key = _clean_key(key)
            records[leaf_key] = value
        records = self._sanitise_get_result(records, path)
        return records

    def update(self, path: str, record: dict):
        self._set_key(path, record)

    def multi_update(self, path: str, record: dict):
        record = flatten(record, reducer="path", max_flatten_depth=2)
        pipeline = self.client.pipeline()
        for key, value in record.items():
            key = f"{path}/{key}"
            self._set_key(key, value, pipeline=pipeline)
        pipeline.execute()

    def remove(self, path: str):
        path = _clean_key(path)
        self.client.delete(path)

    def create_index(self, path: str, field: str):
        try:
            search = self._get_search_client(path, field)
            definition = IndexDefinition(prefix=[path], index_type=IndexType.HASH)
            search.create_index(
                fields=[TextField(field)],
                definition=definition
            )
        except ResponseError:
            print("Requested index already exists!")

    def where(self, path: str, **kwargs):
        assert len(kwargs) == 1, "Searching by only one field value is currently supported!"
        field = list(kwargs.keys())[0]
        value = list(kwargs.values())[0]
        results = self._search(path, field, value)
        results = self._fetch_searched_records(results)
        return results

    def _check_health(self):
        return self.client.ping()

    def _set_key(self, key, record, pipeline=None):
        pipeline = pipeline if pipeline else self.client
        key = _clean_key(key)
        record = _serialise_record(record)
        pipeline.hset(key, mapping=record)

    def _get_key(self, key):
        record = self.client.hgetall(key)
        record = _deserialise_record(record)
        return record

    def _sanitise_get_result(self, records, path):
        if len(records) == 0:
            records = None
        elif len(records) == 1 and records.get(path) is not None:
            # We have a direct match on the queried path, so we just need to
            # return the underlying record itself
            records = records[path]
        else:
            records = {key.replace(f"{path}/", ""): value for key, value in records.items()}
        return records

    def _get_search_client(self, path, field):
        return Search(self.client, index_name=f"{path}_{field}_index")

    def _search(self, path, field, value):
        search = self._get_search_client(path, field)
        results = search.search(f"@{field}:{value}")
        return results

    def _fetch_searched_records(self, results):
        keys = [doc.id for doc in results.docs]
        records = []
        for key in keys:
            record = self._get_key(key)
            records.append(record)
        return records


def _clean_key(key):
    key = key.replace("//", "/")
    key = key.lstrip("/")
    return key


def _serialise_record(record):
    serialised_record = {}
    for key, value in record.items():
        if value is None:
            continue
        value = value if _is_redis_supported_type(value) else _serialise_value(value)
        serialised_record[key] = value
    return serialised_record


def _is_redis_supported_type(value):
    supported_types = [str, int, float]
    return type(value) in supported_types


def _serialise_value(value):
    value = json.dumps(value, default=_ignore_null_values)
    return value


def _ignore_null_values(d):
    return {k: v for k,v in d.items() if v is not None}


def _deserialise_record(record):
    deserialised_record = {}
    for key, value in record.items():
        value = _deserialise_value(value) if type(value) == str else value
        deserialised_record[key] = value
    return deserialised_record


def _deserialise_value(value):
    try:
        value = json.loads(value)
    except json.decoder.JSONDecodeError:
        pass
    return value
