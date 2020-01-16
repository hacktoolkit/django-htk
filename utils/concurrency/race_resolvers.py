"""race_resolvers.py

A bunch of race condition resolvers
"""

# Python Standard Library Imports
import time


def retry_until_not_none(f, max_attempts=5):
    """Retries a function call `f` until its result is not None
    Up to `max_attempts` total attempts
    """
    result = retry_until(f, lambda x: x is not None, initial=None, max_attempts=max_attempts)
    return result

def retry_until(f, until_predicate, initial=None, max_attempts=5):
    """Retries a function call `f` until its result `until_predicate` returns True
    Up to `max_attempts` total attempts
    `initial` is the initial value for the result before any attempts, and should cause `until_predicate` to return False
    """
    result = initial
    attempts = 0
    while not(until_predicate(result)) and attempts < max_attempts:
        if attempts > 0:
            time.sleep(1)
        result = f()
        attempts += 1
    return result
