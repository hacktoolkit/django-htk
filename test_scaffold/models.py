from django.db import models

class TestScaffoldModel(models.Model):
    class Meta:
        abstract = True

class FakeTime(TestScaffoldModel):
    """FakeTime keeps track of only one timestamp (one record) or none
    When testing, if there is a record, the next call to talentral.utils.utcnow() returns this timestamp
    """
    timestamp = models.DateTimeField()

class FakePrelaunch(TestScaffoldModel):
    """FakePrelaunch keeps track of only one boolean (one record) or none
    When testing,  if there is a record, the next call to talentral.utils.is_prelaunch_mode() returns this boolean
    """
    prelaunch_mode = models.BooleanField(default=False)
    prelaunch_host = models.BooleanField(default=False)

class TestScaffold(object):
    # FakeTime
    def clear_fake_timestamp(self):
        fake_time_objects = FakeTime.objects.all()
        for fake_time in fake_time_objects:
            fake_time.delete()

    def get_fake_timestamp(self):
        fake_time_objects = FakeTime.objects.all()
        if len(fake_time_objects):
            timestamp = fake_time_objects[0].timestamp
        else:
            timestamp = None
        return timestamp

    def set_fake_timestamp(self, timestamp):
        self.clear_fake_timestamp()
        fake_time = FakeTime.objects.create(timestamp=timestamp)
        fake_time.save()

    # FakePrelaunch
    def clear_fake_prelaunch(self):
        fake_prelaunch_objects = FakePrelaunch.objects.all()
        for fake_prelaunch in fake_prelaunch_objects:
            fake_prelaunch.delete()

    def get_fake_prelaunch_mode(self):
        fake_prelaunch_objects = FakePrelaunch.objects.all()
        if len(fake_prelaunch_objects):
            prelaunch_mode = fake_prelaunch_objects[0].prelaunch_mode
        else:
            prelaunch_mode = None
        return prelaunch_mode

    def get_fake_prelaunch_host(self):
        fake_prelaunch_objects = FakePrelaunch.objects.all()
        if len(fake_prelaunch_objects):
            prelaunch_host = fake_prelaunch_objects[0].prelaunch_host
        else:
            prelaunch_host = None
        return prelaunch_host

    def set_fake_prelaunch(self, prelaunch_mode=False, prelaunch_host=False):
        self.clear_fake_prelaunch()
        fake_prelaunch = FakePrelaunch.objects.create(
            prelaunch_mode=prelaunch_mode,
            prelaunch_host=prelaunch_host,
        )
        fake_prelaunch.save()
