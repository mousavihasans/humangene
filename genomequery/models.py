from enum import IntEnum

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from utils.intenum import IntEnumField


class GenomeQuery(models.Model):
    name = models.CharField(max_length=200, unique=True, default='genome query')
    price = models.IntegerField(default=2000000, help_text='unit is IRR.')
    code = models.TextField(null=True, blank=True)
    free_daily_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class QueryTypeChoices(IntEnum):
    free_daily = 0
    bought_by_credit = 1
    created_manually = 2


class QueryItem(models.Model):
    genome_query = models.ForeignKey(GenomeQuery, on_delete=models.PROTECT)
    type = IntEnumField(QueryTypeChoices, default=QueryTypeChoices.created_manually)
    response = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name='created_queries')
    created_at = models.DateTimeField(default=now)
    performed_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='performed_queries')
    performed_at = models.DateTimeField(default=now, null=True, blank=True)

    def __str__(self):
        name = str(QueryTypeChoices(self.type).name) + ' for ' + self.performed_by.username
        return name

