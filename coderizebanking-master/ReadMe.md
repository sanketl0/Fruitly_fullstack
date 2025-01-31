## Django Tenant Specific Commands

### For Migrating

To make migrations file

```
python manage.py makemigrations
```

For shared schema only

```
python manage.py migrate_schemas --shared
```

For all schemas

```
python manage.py migrate_schemas
```


## To add new account / Create a new tenant

- Open Django's Shell
```commandline
python manage.py shell
```

- Run all the commands one by one from `create_tenant.py`
```python
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
```

- Then add the details in `BankAPI/post_data_config.py`

```python
if client_name == 'CodeRize':
    variable_data = {"CORPID": "0000000",
                     "USERID": "AAAAAAA",
                     "ACCOUNTNO": "000000000"}
```

- Test the API by running the balance check api
```url
http://localhost:5003/clients/Fruitly/CIBPayment/Balance/Fetch/
```

- Any errors will be logged in `Logger/dev_log_file`