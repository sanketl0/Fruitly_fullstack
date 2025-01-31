import datetime
import traceback

from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from CIBPayment.models import AccountStatement
from CIBPayment.serializers import AccountStatementTransactionsSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from Logger import logger


class TransactionViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]

    @action(detail=False, url_path=r'BetweenDates/(?P<from_date>[^\.]+)/(?P<to_date>[^\.]+)')
    def between_from_and_to_date(self, request, from_date, to_date):
        logger.debug(f'-- API Call -- {request.path} | Headers: {request.headers} | Data: {request.data}')
        transactions = AccountStatement.objects.filter(TXNDATE__date__range=[from_date, to_date])
        serializer = AccountStatementTransactionsSerializer(transactions, many=True)
        return Response(serializer.data)
#
