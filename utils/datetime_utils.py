import datetime

from django.conf import settings
from django.utils.timezone import utc

def utcnow():
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    if settings.TEST:
        from htk.test_scaffold.models import TestScaffold
        scaffold = TestScaffold()
        fake_time = scaffold.get_fake_timestamp()
        if fake_time:
            now = fake_time
    return now
