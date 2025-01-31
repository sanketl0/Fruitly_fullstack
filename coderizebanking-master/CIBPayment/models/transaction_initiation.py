from django.db import models
from .object_log import ObjectLog


class TransactionInitiation(ObjectLog, models.Model):
    id = models.AutoField(primary_key=True)
    # Initiate Transaction
    AGGRID = models.CharField(max_length=50)
    AGGRNAME = models.CharField(max_length=50)
    CORPID = models.CharField(max_length=50)
    USERID = models.CharField(max_length=50)
    URN = models.CharField(max_length=50)
    UNIQUEID = models.CharField(max_length=50)
    DEBITACC = models.CharField(max_length=50)
    CREDITACC = models.CharField(max_length=50)
    IFSC = models.CharField(max_length=50)
    AMOUNT = models.CharField(max_length=50)
    CURRENCY = models.CharField(max_length=50)
    TXNTYPE = models.CharField(max_length=50)
    PAYEENAME = models.CharField(max_length=50)
    REMARKS = models.CharField(max_length=255)
    WORKFLOW_REQD = models.CharField(max_length=50)
    BENLEI = models.CharField(max_length=50)
    CUSTOMERINDUCED = models.CharField(max_length=50)

    # Response from transaction (Success)
    UTRNUMBER = models.CharField(max_length=50, unique=True, null=True)
    REQID = models.CharField(max_length=50, null=True)
    STATUS = models.CharField(max_length=50, null=True)
    RESPONSE = models.CharField(max_length=50, null=True)
    
    class Meta:
        db_table = 'CIBPayment_transactioninitiation'
