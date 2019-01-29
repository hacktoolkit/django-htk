# Python Standard Library Imports
import datetime

# Third Party / PIP Imports

# Django Imports
from django.db import models

# HTK Imports


class TestScaffoldModel(models.Model):
    class Meta:
        abstract = True


class FakeTime(TestScaffoldModel):
    """FakeTime keeps track of only one timestamp (one record) or none
    When testing, if there is a record, the next call to htk.utils.utcnow() returns this timestamp
    """
    timestamp = models.DateTimeField()


class FakePrelaunch(TestScaffoldModel):
    """FakePrelaunch keeps track of only one boolean (one record) or none
    When testing,  if there is a record, the next call to htk.apps.prelaunch.utils.is_prelaunch_mode() returns this boolean
    """
    prelaunch_mode = models.BooleanField(default=False)
    prelaunch_host = models.BooleanField(default=False)


class TestScaffold(object):

    ##
    # FakeTime

    @classmethod
    def clear_fake_timestamp(cls):
        FakeTime.objects.all().delete()

    @classmethod
    def get_fake_timestamp(cls):
        fake_time_objects = FakeTime.objects.all()
        if fake_time_objects.exists():
            timestamp = fake_time_objects.first().timestamp
        else:
            timestamp = None
        return timestamp

    @classmethod
    def set_fake_timestamp(cls, dt=None, timestamp=None):
        """Fakes the system time by setting it to `timestamp`

        Can take either a `datetime.datetime` or Unix timestamp
        """
        assert (dt is not None or timestamp is not None), 'Needs to have at least dt or timestamp specified'
        assert (dt is None or timestamp is None), 'Cannot specify both dt as well as timestamp'

        if dt is None and timestamp is not None:
            dt = datetime.datetime.fromtimestamp(timestamp)

        TestScaffold.clear_fake_timestamp()
        fake_time = FakeTime.objects.create(timestamp=dt)

    ##
    # FakePrelaunch

    @classmethod
    def clear_fake_prelaunch(cls):
        FakePrelaunch.objects.all().delete()

    @classmethod
    def get_fake_prelaunch_mode(cls):
        fake_prelaunch_objects = FakePrelaunch.objects.all()
        if fake_prelaunch_objects.exists():
            prelaunch_mode = fake_prelaunch_objects.first().prelaunch_mode
        else:
            prelaunch_mode = None
        return prelaunch_mode

    @classmethod
    def get_fake_prelaunch_host(cls):
        fake_prelaunch_objects = FakePrelaunch.objects.all()
        if fake_prelaunch_objects.exists():
            prelaunch_host = fake_prelaunch_objects.first().prelaunch_host
        else:
            prelaunch_host = None
        return prelaunch_host

    @classmethod
    def set_fake_prelaunch(cls, prelaunch_mode=False, prelaunch_host=False):
        TestScaffold.clear_fake_prelaunch()
        fake_prelaunch = FakePrelaunch.objects.create(
            prelaunch_mode=prelaunch_mode,
            prelaunch_host=prelaunch_host,
        )
