# Python Standard Library Imports
from dataclasses import dataclass


@dataclass
class TodosConfig:
    """Todos Config

    This class specifies section of the app or codebase to scan for TODOs in.

    `HTK_ADMINTOOLS_TODOS_CONFIGS` will be set to a list of `TodosConfig` objects.
    """

    name: str
    directory: str

    @property
    def key(self):
        key = self.name.lower().replace(' ', '-')
        return key

    @property
    def exclusion_pattern(self):
        return f'{self.directory}/'
