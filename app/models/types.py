# App/Utils/db_types.py
import json

from sqlalchemy.types import TEXT, TypeDecorator


class JsonEncodedDict(TypeDecorator):
    """Represents a Python dict as a JSON-encoded string in the DB."""

    impl = TEXT

    def process_bind_param(self, value, dialect):
        return json.dumps(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return json.loads(value) if value is not None else None
