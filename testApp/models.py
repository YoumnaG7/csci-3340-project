from django.db import models
from djagno.conf import settings

# Create your models here.

class Event(models.Model):
    DAYS = [(0, "Mon"), (1, "Tue"), (2, "Wed"), (3, "Thu"), (4, "Fri")]
    CATEGORIES = [("class", "Class"), ("study", "Study time"), ("social", "Campus & friends")]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100, blank = True)
    category = models.CharField(max_length = 10, choices = CATEGORIES, default = "class")
    day = models.PositiveSmallIntegerField(choices = DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    @property
    def start_offset(self):
        return self.start_time.hour + self.start_time.minute / 60 - 8

    @property
    def duration(self):
        end = self.end_time.hour + self.end_time.minute / 60
        return end - (self.start_time.hour + self.start_time.minute / 60)

class ShareAccess(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shared_with")
    viewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="can_view")