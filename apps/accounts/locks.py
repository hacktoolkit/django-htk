# HTK Imports
from htk.cache.classes import LockableObject
from htk.constants.time import *


class UserEmailRegistrationLock(LockableObject):
    """Lock to prevent race condition of simultaneous regsitration attempts
    """
    def __init__(self, email):
        self.email = email.strip().lower()

    def get_lock_duration(self):
        duration = TIMEOUT_1_MINUTE
        return duration

    def get_lock_key_suffix(self, suffix_resolver=None):
        suffix = '%s' % self.email
        return suffix
