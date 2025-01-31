from django.db import models

from CIBPayment.objs import Remark
from .object_log import ObjectLog


class AccountStatement(ObjectLog, models.Model):
    id = models.AutoField(primary_key=True)

    # Fields in response but not with each transaction
    ACCOUNTNO = models.CharField(max_length=50)

    # Field in transaction response
    TXNDATE = models.DateTimeField()
    REMARKS = models.CharField(max_length=200)
    AMOUNT = models.DecimalField(max_digits=15, decimal_places=2)
    BALANCE = models.DecimalField(max_digits=15, decimal_places=2)
    VALUEDATE = models.DateField()
    TYPE = models.CharField(max_length=50)
    TRANSACTIONID = models.CharField(max_length=50)

    # Reconciliation
    reconciliation_status = models.CharField(max_length=50, default='PENDING')
    remaining_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    bill_count = models.CharField(max_length=50, null=True)
    invoice_count = models.CharField(max_length=50, null=True)

    # Split Remark into useful categories
    remark_main_type = models.CharField(max_length=50, null=True)
    remark_subtype = models.CharField(max_length=50, null=True)
    remark_account_no = models.CharField(max_length=50, null=True)
    remark_IFSC = models.CharField(max_length=50, null=True)
    remark_unsplit = models.CharField(max_length=200, null=True)
    remark_comment = models.CharField(max_length=100, null=True)
    remark_from_bank = models.CharField(max_length=100, null=True)
    remark_payer_name = models.CharField(max_length=50, null=True)
    remark_upi_address = models.CharField(max_length=50, null=True)

    # Match with trader and farmer
    customer_id = models.CharField(max_length=50, null=True)
    customer_name = models.CharField(max_length=50, null=True)
    customer_location = models.CharField(max_length=50, null=True)
    vendor_id = models.CharField(max_length=50, null=True)
    vendor_name = models.CharField(max_length=50, null=True)
    vendor_location = models.CharField(max_length=50, null=True)
    
    class Meta:
        db_table = 'CIBPayment_accountstatement'

    def split_remark(self):
        split_remark = Remark(remark_string=self.REMARKS).split_remarks()

        self.remark_main_type = split_remark.get('remark_main_type')
        self.remark_subtype = split_remark.get('remark_subtype')
        self.remark_account_no = split_remark.get('remark_account_no')
        self.remark_IFSC = split_remark.get('remark_IFSC')
        self.remark_comment = split_remark.get('remark_comment')
        self.remark_from_bank = split_remark.get('remark_from_bank')
        self.remark_payer_name = split_remark.get('remark_payer_name')
        self.remark_upi_address = split_remark.get('remark_upi_address')

        usplit_remark = split_remark.get('remark_unsplit')
        if usplit_remark:
            self.remark_unsplit = str(usplit_remark)
