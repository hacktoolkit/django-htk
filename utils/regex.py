# Python Standard Library Imports
import re


class Re(object):
    def __init__(self):
        self.last_match = None

    @property
    def m(self):
        return self.last_match

    def match(self, pattern, text):
        if type(pattern).__name__ == 'SRE_Pattern':
            self.last_match = pattern.match(text)
        else:
            self.last_match = re.match(pattern, text)
        return self.last_match

    def search(self, pattern, text):
        if type(pattern).__name__ == 'SRE_Pattern':
            self.last_match = pattern.search(text)
        else:
            self.last_match = re.search(pattern, text)
        return self.last_match

    def sub(self, pattern, repl, string, count=0, flags=0):
        def frepl(matchobj):
            self.last_match = matchobj
            return repl

        if type(pattern).__name__ == 'SRE_Pattern':
            result, n = pattern.subn(frepl, string, count=count)
        else:
            result, n = re.subn(
                pattern, frepl, string, count=count, flags=flags
            )
        if n == 0:
            self.last_match = None
        return result


RE = Re()
