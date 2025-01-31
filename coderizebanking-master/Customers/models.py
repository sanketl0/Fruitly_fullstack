from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Client(TenantMixin):
    schema_name = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=100 ,unique=True)
    on_trial = models.BooleanField(default=True)


    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True


class Domain(DomainMixin):
    pass