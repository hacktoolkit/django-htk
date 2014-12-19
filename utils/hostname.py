import re

from htk.utils import htk_setting

def is_dev_host(host):
    """Determines whether `host` is a dev host
    """
    canonical_domain = htk_setting('HTK_CANONICAL_DOMAIN')
    dev_host_regexps = htk_setting('HTK_DEV_HOST_REGEXPS')
    is_dev = False
    for r in dev_host_regexps:
        if re.match(r'%s%s' % (r, canonical_domain,), host):
            is_dev = True
            break
        else:
            pass
    return is_dev
