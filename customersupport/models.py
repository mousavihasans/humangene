from enum import IntEnum

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from humangene import settings
from utils.intenum import IntEnumField


class TaskStateChoices(IntEnum):
    accepted = 0
    in_progress = 1
    completed_with_errors = 2
    completed_successfully = 3


class TrackTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    state = IntEnumField(TaskStateChoices, default=TaskStateChoices.accepted)
    result = models.FileField(upload_to='files/', null=True, blank=True)
    created_at = models.DateTimeField(default=now)
    uploaded_result_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.state == TaskStateChoices.completed_successfully and self.upload_result_at is None:
            raise ValidationError('If the task is completed, you should upload the result.')
        # todo: just 1 week is enough for data.

