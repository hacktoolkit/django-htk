# HTK Imports
from htk.utils import htk_setting


def is_maintenance_mode():
    maintenance_mode = htk_setting('HTK_MAINTENANCE_MODE', False)
    return maintenance_mode
