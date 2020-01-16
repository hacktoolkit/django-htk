# Python Standard Library Imports
import collections
import functools
import types


class memoized(object):
    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).

    From: https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)

class CachedAttribute(object):
    """Computes attribute value and caches it in instance.

    Example:
        class MyClass(object):
            def myMethod(self):
                # ...
            myMethod = CachedAttribute(myMethod)
    Use "del inst.myMethod" to clear cache.

    From: http://code.activestate.com/recipes/276643-caching-and-aliasing-with-descriptors/
    """

    INSTANCE_CACHE_NAME = '_cached_attribute_instances'

    def __init__(self, method, name=None):
        self.method = method
        self.name = name or method.__name__

    def __get__(self, inst, cls):
        """Returns the result of the method this instance decorates.
        The first time this is called, the method will be evaluated
        and its value will be cached in the inst object passed in.
        A method will also be added to the inst object which can
        be used to clear all of the cached attributes for that object.

        Usage:

        class Foo(object):
            @CachedAttribute
            def bar(self):
                return 10

        foo = Foo()

        # will evaluate bar() from above the first time it's used
        print('first', foo.bar)

        # will return the cached value of bar()
        print('second', foo.bar)

        # will remove all of the cached attributes from the foo instance
        foo.clear_all_cached_attributes()

        # will evaluate bar()
        print('third', foo.bar)
        """
        if inst is None:
            return self

        result = self.method(inst)
        setattr(inst, self.name, result)

        # store a list of the attr names that we have cached
        instance_cache = getattr(inst, self.INSTANCE_CACHE_NAME, None)

        # If this is the first cached attribute for this instance, create
        # a clear_all method for the instance which will allow us to flush
        # all of the cached attributes for this instance.
        if instance_cache is None:
            instance_cache = []
            setattr(inst, self.INSTANCE_CACHE_NAME, instance_cache)
            def _clear_all_attributes(target_self):
                while instance_cache:
                    delattr(inst, instance_cache.pop())

            inst.clear_all_cached_attributes = types.MethodType(_clear_all_attributes, inst)

        instance_cache.append(self.name)

        return result

class CachedClassAttribute(object):
    """Computes attribute value and caches it in class.

    Example:
        class MyClass(object):
            def myMethod(cls):
                # ...
            myMethod = CachedClassAttribute(myMethod)
    Use "del MyClass.myMethod" to clear cache.
    """

    def __init__(self, method, name=None):
        self.method = method
        self.name = name or method.__name__

    def __get__(self, inst, cls):
        result = self.method(cls)
        setattr(cls, self.name, result)
        return result


class ReadAliasAttribute(object):
    """If not explcitly assigned this attribute is an alias for other.

    Example:
        class Document(object):
            title='?'
            shortTitle=ReadAliasAttribute('title')
    """
    def __init__(self, name):
        self.name = name

    def __get__(self, inst, cls):
        if inst is None:
            return self
        return getattr(inst, self.name)


class AliasAttribute(ReadAliasAttribute):
    """This attribute is an alias for other.

    Example:
        class Document(object):
            newAttrName=somevalue
            deprecatedAttrName=AliasAttribute('newAttrName')
    """

    def __set__(self, inst, value):
        setattr(inst, self.name, value)

    def __delete__(self, inst):
        delattr(inst, self.name)
