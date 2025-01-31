from rest_framework import viewsets

from CIBPayment.models import TransactionStatus
from CIBPayment.serializers import TransactionStatusSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from Logger import logger


class TransactionStatusViewSet(viewsets.ReadOnlyModelViewSet):
    # authentication_classes = [TokenAuthentication]  # Token Authentication
    permission_classes = [IsAuthenticated]
    queryset = TransactionStatus.objects.all()
    serializer_class = TransactionStatusSerializer
