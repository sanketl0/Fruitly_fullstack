from django.db import models


class ObjectLog(models.Model):
    created_by = models.CharField(max_length=50, default='Unknown')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=50, default='Unknown')
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
