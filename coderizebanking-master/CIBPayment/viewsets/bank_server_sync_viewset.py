from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from CIBPayment.models import BankServerSync
from CIBPayment.serializers import BankServerSyncSerializer

from Logger import logger

class BankServerSyncViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]  # Token Authentication
    permission_classes = [IsAuthenticated]
    lookup_field = 'api'

    def list(self, request):
        logger.debug(f"-- API Call -- {request.path} | Method: {request.method} | Headers: {dict(request.headers)} | Query Params: {request.query_params}")
        logger.debug(f"-- Request Data -- {request.data}")
        
        try:
            server_sync_objects = BankServerSync.objects.all()
            logger.debug(f"-- Retrieved {len(server_sync_objects)} objects from BankServerSync --")
            return Response(BankServerSyncSerializer(server_sync_objects, many=True).data)
        except Exception as e:
            logger.error(f"-- Error retrieving BankServerSync objects: {str(e)} --")
            return Response({"error": str(e)}, status=500)

    def retrieve(self, request, api):
        logger.debug(f"-- API Call -- {request.path} | Method: {request.method} | Headers: {dict(request.headers)} | Query Params: {request.query_params}")
        logger.debug(f"-- Request Data -- {request.data}")
        
        try:
            server_sync_object = BankServerSync.objects.get(api=api)
            logger.debug(f"-- Retrieved object from BankServerSync with api: {api} --")
            return Response(BankServerSyncSerializer(server_sync_object).data)
        except BankServerSync.DoesNotExist:
            logger.warning(f"-- BankServerSync object with api: {api} not found --")
            return Response({"error": "Object not found"}, status=404)
        except Exception as e:
            logger.error(f"-- Error retrieving BankServerSync object: {str(e)} --")
            return Response({"error": str(e)}, status=500)
