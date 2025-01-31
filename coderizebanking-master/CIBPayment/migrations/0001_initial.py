# Generated by Django 4.0.3 on 2025-01-22 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountStatement',
            fields=[
                ('created_by', models.CharField(default='Unknown', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.CharField(default='Unknown', max_length=50)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ACCOUNTNO', models.CharField(max_length=50)),
                ('TXNDATE', models.DateTimeField()),
                ('REMARKS', models.CharField(max_length=200)),
                ('AMOUNT', models.DecimalField(decimal_places=2, max_digits=15)),
                ('BALANCE', models.DecimalField(decimal_places=2, max_digits=15)),
                ('VALUEDATE', models.DateField()),
                ('TYPE', models.CharField(max_length=50)),
                ('TRANSACTIONID', models.CharField(max_length=50)),
                ('reconciliation_status', models.CharField(default='PENDING', max_length=50)),
                ('remaining_amount', models.DecimalField(decimal_places=2, max_digits=15, null=True)),
                ('bill_count', models.CharField(max_length=50, null=True)),
                ('invoice_count', models.CharField(max_length=50, null=True)),
                ('remark_main_type', models.CharField(max_length=50, null=True)),
                ('remark_subtype', models.CharField(max_length=50, null=True)),
                ('remark_account_no', models.CharField(max_length=50, null=True)),
                ('remark_IFSC', models.CharField(max_length=50, null=True)),
                ('remark_unsplit', models.CharField(max_length=200, null=True)),
                ('remark_comment', models.CharField(max_length=100, null=True)),
                ('remark_from_bank', models.CharField(max_length=100, null=True)),
                ('remark_payer_name', models.CharField(max_length=50, null=True)),
                ('remark_upi_address', models.CharField(max_length=50, null=True)),
                ('customer_id', models.CharField(max_length=50, null=True)),
                ('customer_name', models.CharField(max_length=50, null=True)),
                ('customer_location', models.CharField(max_length=50, null=True)),
                ('vendor_id', models.CharField(max_length=50, null=True)),
                ('vendor_name', models.CharField(max_length=50, null=True)),
                ('vendor_location', models.CharField(max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BankServerSync',
            fields=[
                ('created_by', models.CharField(default='Unknown', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.CharField(default='Unknown', max_length=50)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('api', models.CharField(max_length=50)),
                ('last_hit', models.DateTimeField(auto_now=True)),
                ('last_successful_hit', models.DateTimeField(null=True)),
                ('number_of_hits', models.BigIntegerField(default=0)),
                ('recording_since', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'CIBPayment_bankserversync',
            },
        ),
        migrations.CreateModel(
            name='TransactionInitiation',
            fields=[
                ('created_by', models.CharField(default='Unknown', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.CharField(default='Unknown', max_length=50)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('AGGRID', models.CharField(max_length=50)),
                ('AGGRNAME', models.CharField(max_length=50)),
                ('CORPID', models.CharField(max_length=50)),
                ('USERID', models.CharField(max_length=50)),
                ('URN', models.CharField(max_length=50)),
                ('UNIQUEID', models.CharField(max_length=50)),
                ('DEBITACC', models.CharField(max_length=50)),
                ('CREDITACC', models.CharField(max_length=50)),
                ('IFSC', models.CharField(max_length=50)),
                ('AMOUNT', models.CharField(max_length=50)),
                ('CURRENCY', models.CharField(max_length=50)),
                ('TXNTYPE', models.CharField(max_length=50)),
                ('PAYEENAME', models.CharField(max_length=50)),
                ('REMARKS', models.CharField(max_length=255)),
                ('WORKFLOW_REQD', models.CharField(max_length=50)),
                ('BENLEI', models.CharField(max_length=50)),
                ('CUSTOMERINDUCED', models.CharField(max_length=50)),
                ('UTRNUMBER', models.CharField(max_length=50, null=True, unique=True)),
                ('REQID', models.CharField(max_length=50, null=True)),
                ('STATUS', models.CharField(max_length=50, null=True)),
                ('RESPONSE', models.CharField(max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionStatus',
            fields=[
                ('created_by', models.CharField(default='Unknown', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.CharField(default='Unknown', max_length=50)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('AGGRID', models.CharField(max_length=50)),
                ('CORPID', models.CharField(max_length=50)),
                ('USERID', models.CharField(max_length=50)),
                ('UNIQUEID', models.CharField(max_length=50)),
                ('URN', models.CharField(max_length=50)),
                ('STATUS', models.CharField(max_length=50, null=True)),
                ('RESPONSE', models.CharField(max_length=50, null=True)),
                ('UTRNUMBER', models.CharField(max_length=50, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
