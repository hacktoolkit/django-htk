#from abc import ABCMeta
#from abc import abstractmethod

# Django Imports
from django.core.cache import cache

# HTK Imports
from htk.cache.utils import get_cache_key_prefix
from htk.constants.time import *


class CacheableObject(object):
    """Abstract base class for cacheable objects

    Meant to be a secondary base class via multiple inheritance
    http://docs.python.org/tutorial/classes.html#multiple-inheritance

    By subclassing object instead of django.db.models, we are taking a more robust approach such that DB subclasses can extend it if we move away from django.db.models (custom Riak models, etc)
    """

    def get_cache_payload(self):
        """Default payload

        Default value: self

        Can be overridden by a subclass
        """
        payload = self
        return payload

    def get_cache_duration(self):
        """Default cache duration in seconds

        Default value: TIMEOUT_30_MINUTES

        Can be overridden by a subclass
        """
        duration = TIMEOUT_30_MINUTES
        return duration

    def get_cache_key_suffix(self, suffix_resolver=lambda x: x.id):
        """Default cache key suffix

        Can be overridden by the subclass
        """
        suffix = suffix_resolver(self)
        return suffix

    def get_cache_key(self, suffix=None):
        """Default cache key

        A typical cache key that requires the object to have the attribute `id`:
        key = 'appid:%s:%s' % (self.__class__.__name__, self.id,)

        Can be overridden by the subclass
        """
        cache_key_prefix = get_cache_key_prefix()
        if suffix is None:
            suffix = self.get_cache_key_suffix()
        else:
            pass
        key = '%s:%s:%s' % (cache_key_prefix, self.__class__.__name__, suffix,)
        return key

    def invalidate_cache(self):
        """Default cache invalidation method

        TODO: figure out how to make this work: http://www.slideshare.net/mmalone/scaling-django-1393282
        Pownce: instead of deleting, set the cache key to None for a short period of time--they claim there is a small race condition?
        """
        cache_key = self.get_cache_key()
        cache.delete(cache_key)

    def cache_store(self, refresh=False):
        """Default cache store method
        """
        cache_key = self.get_cache_key()
        cache_payload = self.get_cache_payload()
        cache_duration = self.get_cache_duration()
        if refresh:
            # cache.set() will insert or update
            cache.set(cache_key, cache_payload, cache_duration)
        else:
            # use cache.add() instead of cache.set() by default,
            # cache.add() fails if there's already something stored for the key
            cache.add(cache_key, cache_payload, cache_duration)


class LockableObject(object):
    """Abstract base class for lockable objects

    Meant to be a secondary base class via multiple inheritance
    http://docs.python.org/tutorial/classes.html#multiple-inheritance

    By subclassing object instead of django.db.models, we are taking a more robust approach such that DB subclasses can extend it if we move away from django.db.models (custom Riak models, etc)
    """
    def get_lock_duration(self):
        """Default lock duration in seconds

        Default value: TIMEOUT_5_MINUTES
        Should be indefinite until the lock is released by the owner, but 5 minutes is enough for practical purposes and in case the owner does not properly release the lock

        Can be overridden by a subclass
        """
        duration = TIMEOUT_5_MINUTES
        return duration

    def get_lock_key_suffix(self, suffix_resolver=lambda x: x.id):
        """Default lock key suffix

        Can be overridden by the subclass
        """
        suffix = suffix_resolver(self)
        return suffix

    def get_lock_key(self, suffix=None):
        """Default lock key

        A typical lock key that requires the object to have the attribute `id`:
        key = 'appid:lock:%s:%s' % (self.__class__.__name__, self.id,)

        Can be overridden by the subclass
        """
        cache_key_prefix = get_cache_key_prefix()
        if suffix is None:
            suffix = self.get_lock_key_suffix()
        else:
            pass
        key = '%s:lock:%s:%s' % (cache_key_prefix, self.__class__.__name__, suffix,)
        return key

    def is_locked(self):
        lock_key = self.get_lock_key()
        lock_presence = cache.get(lock_key)
        locked = lock_presence == 1
        return locked

    def acquire(self):
        """Alias for lock()
        """
        return self.lock()

    def release(self):
        """Alias for unlock()
        """
        self.unlock()

    def lock(self):
        """Lock an object, blocking concurrent access
        """
        lock_key = self.get_lock_key()
        lock_duration = self.get_lock_duration()
        # use cache.add() instead of cache.set() by default,
        # cache.add() fails if there's already something stored for the key
        was_locked = cache.add(lock_key, 1, lock_duration)
        return was_locked

    def unlock(self):
        """Unlock the object for concurrent access
        """
        lock_key = self.get_lock_key()
        cache.delete(lock_key)


class CustomCacheScheme(object):
    """Abstract base class for custom cache schemes

    `prekey` A list of values used to compute the eventual cache key.
             Similar to a prehash -> hash
    """
    def __init__(self, prekey=None):
        if prekey is not None:
            if hasattr(prekey, '__iter__'):
                # a list or tuple
                self.prekey = prekey
            else:
                self.prekey = [prekey,]
        else:
            self.prekey = ['default',]
        self._cache_key = None

    def get_cache_key_suffix(self):
        """Cache key suffix based on the prekey

        `prekey` is a list of values

        Can be overridden by the subclass
        """
        key = '-'.join([x.encode("hex") for x in self.prekey])
        return key

    def get_cache_key(self):
        """Default cache key

        Can be overridden by the subclass
        """
        if self._cache_key is None:
            cache_key_prefix = get_cache_key_prefix()
            suffix = self.get_cache_key_suffix()
            self._cache_key = '%s:%s:%s' % (cache_key_prefix, self.__class__.__name__, suffix,)
        return self._cache_key

    def get_cache_payload(self):
        """Default payload

        Default value: True

        Can be overridden by a subclass
        """
        payload = True
        return payload

    def get_cache_duration(self):
        duration = TIMEOUT_30_MINUTES
        return duration

    def get(self):
        cache_key = self.get_cache_key()
        value = cache.get(cache_key)
        return value

    def invalidate_cache(self):
        cache_key = self.get_cache_key()
        cache.delete(cache_key)

    def cache_store(self, payload=None, duration=None):
        if payload is None:
            payload = self.get_cache_payload()
        cache_key = self.get_cache_key()
        duration = self.get_cache_duration() if duration is None else duration
        cache.set(cache_key, payload, duration)
