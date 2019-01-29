# Python Standard Library Imports
import time
from functools import wraps

# Third Party / PIP Imports

# Django Imports

# HTK Imports


class rate_limit_instance_method(object):
    """Instance Method rate-limiter using token bucket algorithm

    See:
    - https://en.wikipedia.org/wiki/Token_bucket
    - https://stackoverflow.com/a/668327/865091
    """
    def __init__(self, rate=1, per=60):
        """Messages added at `rate` messages per `per` seconds

        Default: 1 message per 60 seconds
        """
        self.rate = rate * 1.0
        self.per = per * 1.0

    def __call__(self, instance_method):
        @wraps(instance_method)
        def wrapped(*args, **kwargs):
            # TODO: somehow this decorator turns `instance_method` into a `function`, which loses its `__self__` attribute
            # the workaround (?) is to assume that the first argument to the function is the `instance` (which makes sense)
            instance = getattr(
                instance_method,
                '__self__',
                getattr(
                    instance_method,
                    'im_self',
                    None
                )
            ) or args[0]
            assert(instance is not None)

            # set up buckets per instance method
            if not hasattr(instance, '_rate_limiters'):
                # create new collection of buckets
                instance._rate_limiters = {}

            fn_name = instance_method.__name__
            if fn_name not in instance._rate_limiters:
                # create new bucket
                bucket = {
                    'allowance' : self.rate,
                    'last_check' : time.time(),
                }
                instance._rate_limiters[fn_name] = bucket

            bucket = instance._rate_limiters[fn_name]

            # perform checks
            current = time.time()
            time_passed = current - bucket['last_check']
            bucket['last_check'] = current
            bucket['allowance'] += time_passed * (self.rate / self.per)

            if bucket['allowance'] > rate:
                # throttle
                bucket['allowance'] = rate

            if bucket['allowance'] < 1.0:
                # discard message, do nothing
                pass
            else:
                # forward message
                instance_method(*args, **kwargs)
                bucket['allowance'] -= 1.0
        return wrapped
