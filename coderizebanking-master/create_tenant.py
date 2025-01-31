from Customers.models import Client, Domain

# create your first real tenant
tenant = Client(schema_name='CodeRize',name='CodeRize', on_trial=False)
tenant.save() # migrate_schemas automatically called, your tenant is ready to be used!

# Add one or more domains for the tenant
domain = Domain()
domain.domain = 'CodeRize' # don't add your port or www here!
domain.tenant = tenant
domain.is_primary = True
domain.save()