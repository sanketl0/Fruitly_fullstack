from django.db import models
from .object_log import ObjectLog


class BankServerSync(ObjectLog, models.Model):
    id = models.AutoField(primary_key=True)

    api = models.CharField(max_length=50)
    last_hit = models.DateTimeField(auto_now=True)
    last_successful_hit = models.DateTimeField(null=True)
    number_of_hits = models.BigIntegerField(default=0)
    recording_since = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'CIBPayment_bankserversync'
