from django.db import models
from .object_log import ObjectLog


class TransactionStatus(ObjectLog, models.Model):
    id = models.AutoField(primary_key=True)

    AGGRID = models.CharField(max_length=50)
    CORPID = models.CharField(max_length=50)
    USERID = models.CharField(max_length=50)
    UNIQUEID = models.CharField(max_length=50)
    URN = models.CharField(max_length=50)

    STATUS = models.CharField(max_length=50, null=True)
    RESPONSE = models.CharField(max_length=50, null=True)
    UTRNUMBER = models.CharField(max_length=50, unique=True, null=True)
    
    class Meta:
        db_table = 'CIBPayment_transactionstatus'
