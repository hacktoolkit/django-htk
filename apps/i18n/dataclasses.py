# Python Standard Library Imports
from dataclasses import (
    dataclass,
    field,
)


@dataclass
class LocalizationUsageCheck:
    """Localization Usage Check

    This class specifies section of the app or codebase to scan for l10n strings in.

    `HTK_ADMINTOOLS_LOCALIZATION_USAGE_CHECKS` will be set to a list of `LocalizationUsageCheck` objects.
    """

    name: str
    directory: str
    namespaces: list[str] = field(default_factory=list)
