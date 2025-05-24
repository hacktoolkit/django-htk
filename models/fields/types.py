# Third Party (PyPI) Imports
from ulid import ULID as PYTHON_ULID


class ULID(PYTHON_ULID):
    """ULID class that extends the `ulid.ULID` class with additional methods
    for JSON serialization and encoding.
    """

    def json_encode(self):
        return str(self)
