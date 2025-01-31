# from django.db import models

# class Balance(models.Model):
#     client_name = models.CharField(max_length=255)
#     balance = models.DecimalField(max_digits=12, decimal_places=2)
#     last_updated = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'CIBPayment_balance'


#     def __str__(self):
#         return f"{self.client_name} - {self.balance}"
