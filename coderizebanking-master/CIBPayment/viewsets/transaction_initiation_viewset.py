import traceback
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from CIBPayment.models import TransactionInitiation
from CIBPayment.serializers import TransactionInitiationSerializer

from Logger import logger
import BankAPI


class TransactionInitiationViewSet(viewsets.ReadOnlyModelViewSet):
    # authentication_classes = [TokenAuthentication]  # Token Authentication
    permission_classes = [IsAuthenticated]
    queryset = TransactionInitiation.objects.all()
    serializer_class = TransactionInitiationSerializer

    # For documentation
    @swagger_auto_schema(method="POST", request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "CREDITACC": openapi.Schema(type=openapi.TYPE_STRING),
            "IFSC": openapi.Schema(type=openapi.TYPE_STRING),
            "AMOUNT": openapi.Schema(type=openapi.TYPE_NUMBER, description='decimal, 2places'),
            "TXNTYPE": openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))
    @action(detail=False, methods=(['POST']), url_path='Initiate')
    def initiate_transaction(self, request):
        if request.method == 'POST':
            logger.debug(f'-- API Call -- {request.path} | Headers: {request.headers} | Data: {request.data}')

            # Create post data object to be sent to bank server
            try:
                to_account = request.data['CREDITACC']
                ifsc = request.data['IFSC']
                amount = float(request.data['AMOUNT'])
                transaction_type = request.data['TXNTYPE']
            except KeyError as e:
                return Response(f"Missing field: {e}", status=400)
            except ValueError as e:
                return Response(str(e), status=400)

            post_data = {
                "AGGRID": "OTOE0480",
                "AGGRNAME": "FRUITLY",
                "CORPID": "PRACHICIB1",
                "USERID": "USER3",
                "URN": "SR213835043",
                "UNIQUEID": "43566789699756",
                "DEBITACC": "000451000301",
                "CREDITACC": str(to_account),
                "IFSC": str(ifsc),
                "AMOUNT": f"{amount:.2f}",
                "CURRENCY": "INR",
                "TXNTYPE": transaction_type,
                "PAYEENAME": "FruitlyTest"
            }

            try:
                api = BankAPI.TransactionAPI(data=post_data)
                response = api.call()
                if 200 <= response.status_code <= 299:
                    # Decrypt and save the response only when data is successfully received.
                    decrypted_response = api.decrypt_response_data(method='Basic')
                    post_data.update(decrypted_response)

                    # Save the transaction data to database.
                    serializer = TransactionInitiationSerializer(data=post_data)
                    if serializer.is_valid():
                        serializer.save()
                        logger.info(f"Saved: {serializer.data}")
                        return Response(serializer.data, status=201)
                    else:
                        logger.error(str(serializer.errors))
                        return Response(serializer.errors, status=400)
                else:
                    logger.error(
                        f"Error response: {response.text} | status_code: {response.status_code}")
                    return Response(response.text, status=response.status_code)

            except Exception as e:
                logger.error(traceback.format_exc())
                return Response(str(e), status=500)

        elif request.method == 'GET':
            sample_data = {
                "CREDITACC": "000405002777",
                "IFSC": "ICIC0000011",
                "AMOUNT": 450.23,
                "TXNTYPE": "TPA",
            }
            return Response(sample_data)
