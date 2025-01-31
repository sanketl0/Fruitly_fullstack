from Customers.models import Client, Domain


def create_first_tenant():
    # create your public tenant
    tenant = Client(schema_name='public',name='CodeRizeMaster',on_trial=False)
    tenant.save()

    # Add one or more domains for the tenant
    domain = Domain()
    domain.domain = 'beta.fruitly.co.in'  # don't add your port or www here! on a local server you'll want to use localhost here
    domain.tenant = tenant
    domain.is_primary = True
    domain.save()


def create_real_tenants(name):
    # create your first real tenant
    tenant = Client(schema_name=name,
                    name=name,
                    on_trial=True)
    tenant.save()  # migrate_schemas automatically called, your tenant is ready to be used!

    # Add one or more domains for the tenant
    domain = Domain()
    domain.domain = f'{name.lower()}.beta.fruitly.co.in'  # don't add your port or www here!
    domain.tenant = tenant
    domain.is_primary = True
    domain.save()


create_real_tenants(name='Fruitly')
# create_real_tenants(name='CodeRize')
# create_real_tenants(name='FruitBet')

# create_first_tenant()