
import base64
import datetime
import traceback

from django.utils import timezone
import json
import requests
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response


from CIBPayment.models import BankServerSync
#from CIBPayment.models.balance import Balance
import logging
import BankAPI
from Logger import logger
from BankAPI.post_data_config import PostData
from rest_framework.authentication import TokenAuthentication
from accounts.permission import IsUser1
from rest_framework.permissions import IsAuthenticated
logger = logging.getLogger(__name__)
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Random import get_random_bytes



# class BalanceViewSet(viewsets.ViewSet):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated, IsUser1]
    
#     @action(detail=False, url_path='Fetch')
#     def fetch_balance(self, request):
#         client_name = getattr(request, 'tenant', None)
#         print(request.user)
#         print(request.headers)

#         if client_name:
#             client_name = client_name.name
#             print(f"Tenant: {client_name}")
#         else:
#             print("Tenant information is missing in the request.")
#             return Response({"error": "Tenant information is missing."}, status=400)

#         try:
#             # Prepare the data to be sent to the external API
#             post_data = PostData(client_name=client_name).get_for_balance_fetch()
#             print(f"Payload Data: {post_data}")
#             print("Request headers:", request.headers)

#             # Initialize the BalanceInquiryAPI with the necessary post data
#             api = BankAPI.BalanceInquiryAPI(data=post_data)

#             # Make the API call
#             response = api.call()  # Assuming `call` is correctly implemented to make the actual HTTP request

#             print("API Response Data:", api.call)
#             print("API Response Headers:", api.headers)
#             print("API Response Text:", response.text)
#             print("__api response status code__",response.status_code)

#             # Log the raw response data for debugging
#             logger.debug(f"Raw API Response: {response.text}")
#             logger.debug(f"Full API Response: {response.status_code}")

#             # Attempt to parse the response (assuming it's JSON)
# #            try:
# #                logger.debug(f"Raw Response Data: {response.text}")
# #                response_data = response.json()
# #            except ValueError:
# #                logger.error("Invalid JSON response received.")
# #                return Response({"error": "Invalid JSON response from API."}, status=500)

#             # Update the server sync information
#             server_sync_object, created = BankServerSync.objects.get_or_create(api='BalanceInquiryAPI')
#             server_sync_object.number_of_hits += 1
#             server_sync_object.save()

#             # Check the response status
#             if 200 <= response.status_code <= 299:
#                 # Decrypt the response data
#                 decrypted_response = api.decrypt_response_data(method='Basic')

#                 logger.debug(f"Decrypted response: {decrypted_response}")
#                 print(f"Decrypted response: {decrypted_response}")
#                 balance =decrypted_response.get("EFFECTIVEBAL","N/A")
#                 date = decrypted_response.get("DATE","N/A")
#                 new_response={ 
#                        "EFFECTIVEBAL" :balance ,
#                        "DATE" :date}
#                 # Handle the decrypted response based on its content
#                 if decrypted_response.get("RESPONSE") == "FAILURE":
#                     logger.error("API response indicates failure.")
#                     return Response(decrypted_response, status=500)
#                 else:
#                     # Update the sync information and return the response
#                     server_sync_object.last_successful_hit = timezone.now()
#                     server_sync_object.save()
#                     decrypted_response['last_successful_hit'] = str(
#                         timezone.localtime(server_sync_object.last_successful_hit)
#                     )
#                     return Response(new_response)
#             else:
#                 # Log the error and return failure response
#                 logger.error(f"API call returned non-success status: {response.status_code}")
#                 logger.error(f"API Error Response: {response.text}")
#                 return Response({"error": response_data, "message": "API returned an error."}, status=response.status_code)

#         except requests.exceptions.RequestException as req_err:
#             # Handle request exceptions
#             logger.error("Request failed: %s", str(req_err))
#             return Response({"error": "Request failed.", "details": str(req_err)}, status=500)

#         except Exception as e:
#             # General exception handling
#             logger.error("Error in fetch_balance: %s", str(e))
#             return Response({"error": str(e), "message": "Internal server error occurred."}, status=500)


class BalanceViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated ,IsUser1]
    
    @action(detail=False, url_path='Fetch')
    def fetch_balance(self, request):    
        client_name = getattr(request, 'tenant', None)
        print(request.user)  
        print(request.headers)

        if client_name:
            client_name = client_name.name
            print(f"Tenant: {client_name}")
        else:
            print("Tenant information is missing in the request.")
            return Response({"error": "Tenant information is missing."}, status=400)

        try:
            post_data = PostData(client_name=client_name).get_for_balance_fetch()
            print(f"Payload Data: {post_data}")
            print("request header", request.headers)

            # Hardcoded Encrypted Response (Base64 encoded)
            encrypted_response = """VUT/ydJM9swrehSwJoJm19YAHqvX3+bP7/rtzOLIiM0HDGH0PKvohIcEtFlD73YSMHAfhIK/CDrAh03bUij65kuBoipSs2XEtL4HXVCNkMKF2SJP86ftajEUKrDLldyA7fsnpGDIJBgnHfZ5Yo1od2meAsggN54xbVrzt8ZaqTeF7cpSo61TGiuSz64qOYcP64cPyR1NwjTqtcJbkiElf3ihe37ArWjAiPxAjr10WoujU0EUbjjMNsRzAQoDVIXmVRjxnW0WMpj0R7IFOAU9Fjt6QfRotdKkpHKLx8lBUB7Goq1J6AbZmQ26bEjfIc/87Xlq3G52mSAOZYgV6mfxnNglWRN2Qh/7WynKVyGlxk1OWbAtMu5n9C57Mk3qO7Ismmh1FsI5rpVZ/5kFJm+w7CLFqpYBZI/4FZCvkfIVi8dRgJfDBU38ioLsaOMotWgHN1WsiEcbt/u31c44X0QW1RcABowSznixIWklfQaCXxH2aC7MKjbdD8XHrW0QAeOWsbCBZ0i7LtrxI4+EAZoD+5sc8gcY4thuARnUu9dioTsEmoNe1GSfr52K3HJzc4LeEo5pziw4NdO4X9pJ5aNICS4/DUvJWdSiIVMo9OCs2y+qkEy/RY3KeUefrUMT4Kw3IHx/vpvqloOCAeh+DB62U55cuH/TTEmTj3UJrxxjNEM=""" 

            # Instead of manually decrypting, use your existing decrypt_response_data method
            api = BankAPI.BalanceInquiryAPI(data=post_data)  # Initialize API object
            api.response = type('Response', (object,), {
                'text': encrypted_response,
                'status_code': 200  # Simulating a successful status code
            })()  # Set the response.text and status_code manually

            print("request status____", api.response.status_code)

            decrypted_response = api.decrypt_response_data(method='Basic')

            # Log the decrypted response
            logger.debug(f"Decrypted response: {decrypted_response}")
            print(f"Decrypted response: {decrypted_response}")

            # Check if the response indicates failure
            if decrypted_response.get("RESPONSE") == "FAILURE":
                logger.error("API response indicates failure.")
                return Response(decrypted_response, status=500)
            
            else:
                # If successful, return the decrypted response
                return Response(decrypted_response)

        except Exception as e:
            logger.error("Error in fetch_balance: %s", str(e))
            return Response({"error": str(e), "message": "Internal server error occurred."}, status=500)  
    