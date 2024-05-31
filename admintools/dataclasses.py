# Python Standard Library Imports
import typing as T
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


@dataclass
class AdminToolsEntry:
    """Admin Tools Entry

    This class specifies an admin tool.
    """

    name: str
    url_name: str
    url_params: T.Optional[str] = ''
    new_window: bool = False
    should_render: bool = False


@dataclass
class AdminToolsGroup:
    """Admin Tools Group

    This class specifies a group of admin tools.
    """

    name: str
    icon: str
    tools: list[AdminToolsEntry]
