from rest_framework import serializers

from .models import AccountStatement, BankServerSync, TransactionStatus, TransactionInitiation


class AccountStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountStatement
        fields = '__all__'
        


class AccountStatementUpdateStatementSerializer(serializers.ModelSerializer):
    TXNDATE = serializers.DateTimeField(input_formats=['%d-%m-%Y %H:%M:%S'])
    VALUEDATE = serializers.DateField(input_formats=['%d-%m-%Y'])

    class Meta:
        model = AccountStatement
        fields = ['ACCOUNTNO', 'TXNDATE', 'REMARKS', 'AMOUNT',
                  'BALANCE', 'VALUEDATE', 'TYPE', 'TRANSACTIONID', 'created_by']


class AccountStatementTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountStatement
        fields = ['ACCOUNTNO', 'TXNDATE', 'REMARKS', 'AMOUNT',
                  'BALANCE', 'VALUEDATE', 'TYPE', 'TRANSACTIONID']


class TransactionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionStatus
        fields = '__all__'


class TransactionInitiationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionInitiation
        fields = '__all__'


class BankServerSyncSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankServerSync
        fields = '__all__'


