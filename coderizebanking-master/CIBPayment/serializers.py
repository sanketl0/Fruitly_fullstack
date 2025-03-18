from rest_framework import serializers

from .models import AccountStatement, BankServerSync, TransactionStatus, TransactionInitiation


class AccountStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountStatement
        fields = '__all__'
        read_only_fields = ['transaction_type']  
        
    def to_representation(self, instance):
        """Customize the response based on user role."""
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.user.role != 'user1':
            data.pop('transaction_type', None) 

        return data

    def validate(self, data):
        """Restrict modification of 'transaction_type' to only user1."""
        request = self.context.get('request')

        if request and request.user.role != 'user1' and 'transaction_type' in data:
            raise serializers.ValidationError({"transaction_type": "You are not allowed to modify this field."})

        return data
        


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


