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
import logging
import BankAPI
from Logger import logger
from BankAPI.post_data_config import PostData
from rest_framework.authentication import TokenAuthentication
from accounts.permission import IsUser1
from rest_framework.permissions import IsAuthenticated
logger = logging.getLogger(__name__)



 
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
#             try:
#                 logger.debug(f"Raw Response Data: {response.text}")
#                 response_data = response.json()
#             except ValueError:
#                 logger.error("Invalid JSON response received.")
#                 return Response({"error": "Invalid JSON response from API."}, status=500)

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
#                     return Response(decrypted_response)
#             else:
#                 # Log the error and return failure response
#                 logger.error(f"API call returned non-success status: {response.status_code}")
#                 logger.error(f"API Error Response: {response.text}")
#                 return Response({"error": response_data, "message": "API returned an error."}, status=response.status_code) # type: ignore

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
    
    






















# class BalanceViewSet(viewsets.ViewSet):
    
#     @action(detail=False, url_path='Fetch')
#     def fetch_balance(self, request):
#         client_name = getattr(request, 'tenant', None)
#         logger.debug(f"Request User: {request.user}")
#         logger.debug(f"Request Headers: {request.headers}")

#         if client_name:
#             client_name = client_name.name
#             logger.debug(f"Tenant: {client_name}")
#         else:
#             logger.error("Tenant information is missing in the request.")
#             return Response({"error": "Tenant information is missing."}, status=400)

#         try:
#             post_data = PostData(client_name=client_name).get_for_balance_fetch()
#             logger.debug(f"Payload Data: {post_data}")
            
#             # Call the BalanceInquiryAPI
#             api = BankAPI.BalanceInquiryAPI(data=post_data)
#             response = api.call()
            
#             # logger.debug(f"API Response: {response.text}")
            
#             # # Attempt to parse JSON response
#             # try:
#             #     response_data = response.json()
#             # except ValueError:
#             #     logger.error("Invalid JSON response received.")
#             #     return Response({"error": "Invalid JSON response from API."}, status=500)

#             # Update the API being hit
#             server_sync_object, created = BankServerSync.objects.get_or_create(api='BalanceInquiryAPI')
#             server_sync_object.number_of_hits += 1
#             server_sync_object.save()

#             # Handle the API response
#             if True : #200 <= response.status_code <= 299:
#                 encrypted_base64 = self.encrypt_response()
                
#                 decrypted_response = self.my_decrypt_response_data(encrypted_base64, private_key_file='C:/Users/sanke/Desktop/payment/coderizebanking-master/keys/privkey.pem')
#                 # decrypted_response = api.decrypt_response_data(method='Basic')
#                 logger.debug(f"Decrypted response: {decrypted_response}")

#                 if decrypted_response.get("RESPONSE") == "FAILURE":
#                     logger.error("API response indicates failure.")
#                     return Response(decrypted_response, status=500)
                
#                 else:
#                     server_sync_object.last_successful_hit = timezone.now()
#                     server_sync_object.save()
#                     decrypted_response['last_successful_hit'] = str(
#                         timezone.localtime(server_sync_object.last_successful_hit)
#                     )
#                     return Response(decrypted_response)
#             else:
#                 logger.error(f"API call returned non-success status: {response.status_code}")
#                 logger.error(f"API Error Response: {response.text}")
#                 return Response({"error": response_data, "message": "API returned an error."}, status=response.status_code)

#         except requests.exceptions.RequestException as req_err:
#             logger.error("Request failed: %s", str(req_err), exc_info=True)
#             return Response({"error": "Request failed.", "details": str(req_err)}, status=500)

#         except Exception as e:
#             logger.error("Error in fetch_balance: %s", str(e), exc_info=True)
#             return Response(
#                 {"error": str(e), "message": "Internal server error occurred."},
#                 status=500
#             )

#     # Method to encrypt hardcoded response
#     def encrypt_response(self):
#         hardcoded_response = "hd3Edl+bUhIY/GeC3Em4nxTHDlvUy43gFHxK8O2RJ4qfeVXWZHDa0q4jzI2JpHPJgtLKWooAYwTedcYkmI8R0d84NYbJs2Fq6jVxDRMk2EyGe0sMMlAAP3exwDzU9mih0q0gJhddCD6IW49auzzlDRABLIHYzfQMILMgTGjt1ITO9A+hKiNZyqsy/JdBQCYHFXV7bZMarKBcYHRU/bJcTAmTRUNPOSbiPIa29te+S7MoM9XXJzRTmaB60FM3W0dva4SB4LWQ6LGioY48T6TLpPL9Cn/UBxNUjBze+pNyjZ0JX4slkLMHFUSTPb94ke3ewr+Rj5ptQCzxwrwMOzoJu94bpKPoXmISBcB53XGf22JYn/UQ9FeY1TLxxKGdQJbi9hotCnb9+P6iGL+Hk/7O7/wmX9Bqpo4VqnKxwdN2pncvrdNd1B1CFnVisOs+zNqHXYIZ3ZrexUHVhfyfgcFDrUxAbf4bSGLji2uMiuOIglmy53oGFFdzowUpp64xPMeakIJFAx6bGEaoP/EZoWI12kXFpYglW5JMIDLQ2LrXEPJy8Rr5+MwzSjtAYrVhLMELrWPrcdNK+oq24OvPVVxsCkghXB12Wahs0XZ0r8hDhHJVoCZ3kcKlGLsNqgyDdCFOnKlzOXC6JiLBgDMisXS0hvHjDo2kjuVaP1HqONWFGvk="
#         return hardcoded_response

#     # Method to decrypt the encrypted data
#     def my_decrypt_response_data(self, encrypted_base64, private_key_file):
#         try:
#             encrypted_data = base64.b64decode(encrypted_base64)
#             with open(private_key_file, 'rb') as file:
#                 private_key = RSA.importKey(file.read())
#             decrypter = PKCS1_v1_5.new(private_key)
#             sentinel = get_random_bytes(16)
#             decrypted_data = decrypter.decrypt(encrypted_data, sentinel)
#             if not decrypted_data:
#                 logger.error("Decryption returned empty data.")
#                 raise ValueError("Decryption failed due to empty data.")
#             decrypted_payload = json.loads(decrypted_data.decode('UTF-8'))
#             logger.debug("Decrypted Payload: %s", decrypted_payload)
#             return decrypted_payload
#         except Exception as e:
#             logger.error("Decryption failed: %s", str(e), exc_info=True)
#             raise ValueError(f"Decryption failed: {str(e)}")





# class BalanceViewSet(viewsets.ViewSet):
    
#     @action(detail=False, url_path='Fetch')
#     def fetch_balance(self, request):
#         client_name = getattr(request, 'tenant', None)
#         logger.debug(f"Request User: {request.user}")
#         logger.debug(f"Request Headers: {request.headers}")

#         if client_name:
#             client_name = client_name.name
#             logger.debug(f"Tenant: {client_name}")
#         else:
#             logger.error("Tenant information is missing in the request.")
#             return Response({"error": "Tenant information is missing."}, status=400)

#         try:
#             post_data = PostData(client_name=client_name).get_for_balance_fetch()
#             logger.debug(f"Payload Data: {post_data}")
            
#             # Call the BalanceInquiryAPI
#             api = BankAPI.BalanceInquiryAPI(data=post_data)
#             response = api.call()
            
#             # Update the API being hit
#             server_sync_object, created = BankServerSync.objects.get_or_create(api='BalanceInquiryAPI')
#             server_sync_object.number_of_hits += 1
#             server_sync_object.save()

#             # Handle the API response
#             if 200 <= response.status_code <= 299:
#                 encrypted_base64 = self.encrypt_response(response.text)
                
#                 decrypted_response = self.my_decrypt_response_data(encrypted_base64, private_key_file='C:/Users/sanke/Desktop/payment/coderizebanking-master/keys/privkey.pem')
#                 logger.debug(f"Decrypted response: {decrypted_response}")

#                 if decrypted_response.get("RESPONSE") == "FAILURE":
#                     logger.error("API response indicates failure.")
#                     return Response(decrypted_response, status=500)
                
#                 else:
#                     server_sync_object.last_successful_hit = timezone.now()
#                     server_sync_object.save()
#                     decrypted_response['last_successful_hit'] = str(
#                         timezone.localtime(server_sync_object.last_successful_hit)
#                     )
#                     return Response(decrypted_response)
#             else:
#                 logger.error(f"API call returned non-success status: {response.status_code}")
#                 logger.error(f"API Error Response: {response.text}")
#                 return Response({"error": response.text, "message": "API returned an error."}, status=response.status_code)

#         except requests.exceptions.RequestException as req_err:
#             logger.error("Request failed: %s", str(req_err), exc_info=True)
#             return Response({"error": "Request failed.", "details": str(req_err)}, status=500)

#         except Exception as e:
#             logger.error("Error in fetch_balance: %s", str(e), exc_info=True)
#             return Response(
#                 {"error": str(e), "message": "Internal server error occurred."},
#                 status=500
#             )

#     # Method to encrypt the actual API response
#     def encrypt_response(self, api_response):
#         try:
#             # Encrypt the actual response text
#             encrypted_data = self.encrypt_with_rsa(api_response)
#             return encrypted_data
#         except Exception as e:
#             logger.error("Encryption failed: %s", str(e), exc_info=True)
#             raise ValueError(f"Encryption failed: {str(e)}")
    
#     # Method to perform encryption using RSA
#     def encrypt_with_rsa(self, data):
#         try:
#             # Encrypt the response using RSA encryption
#             public_key = RSA.importKey(open('path_to_public_key.pem', 'rb').read())  # Load your public key
#             encryptor = PKCS1_v1_5.new(public_key)
#             encrypted_data = encryptor.encrypt(data.encode('utf-8'))
#             encrypted_base64 = base64.b64encode(encrypted_data).decode('utf-8')
#             return encrypted_base64
#         except Exception as e:
#             logger.error("Encryption failed during RSA process: %s", str(e), exc_info=True)
#             raise ValueError(f"Encryption failed: {str(e)}")

#     # Method to decrypt the encrypted response data
#     def my_decrypt_response_data(self, encrypted_base64, private_key_file):
#         try:
#             # Base64 decode the encrypted data
#             encrypted_data = base64.b64decode(encrypted_base64)
            
#             # Load the private key
#             with open(private_key_file, 'rb') as file:
#                 private_key = RSA.importKey(file.read())
            
#             # Create a decryption object
#             decrypter = PKCS1_v1_5.new(private_key)
            
#             # Set a random sentinel value for decryption
#             sentinel = get_random_bytes(16)
            
#             # Decrypt the data
#             decrypted_data = decrypter.decrypt(encrypted_data, sentinel)
            
#             # If decryption failed (empty data), log the error
#             if not decrypted_data:
#                 logger.error("Decryption returned empty data.")
#                 raise ValueError("Decryption failed due to empty data.")
            
#             # Convert decrypted bytes to string and parse as JSON
#             decrypted_payload = json.loads(decrypted_data.decode('UTF-8'))
            
#             # Log the decrypted data
#             logger.debug("Decrypted Payload: %s", decrypted_payload)
            
#             return decrypted_payload
        
#         except Exception as e:
#             logger.error("Decryption failed: %s", str(e), exc_info=True)
#             raise ValueError(f"Decryption failed: {str(e)}")



















# class BalanceViewSet(viewsets.ViewSet):
    # authentication_classes = [TokenAuthentication]  
    # permission_classes = [IsAuthenticated ,IsUser1OrAdmin]
    
    # @action(detail=False, url_path='Fetch')
    # def fetch_balance(self, request):
    #     client_name = getattr(request, 'tenant', None)
    #     print(request.user)  # Check if the token maps to a valid user
    #     print(request.headers)

    #     if client_name:
    #         client_name = client_name.name
    #         print(f"Tenant: {client_name}")
    #     else:
    #         print("Tenant information is missing in the request.")
    #         return Response({"error": "Tenant information is missing."}, status=400)

    #     try:
    #         post_data = PostData(client_name=client_name).get_for_balance_fetch()
    #         print(f"Payload Data: {post_data}")

    #         # Call the BalanceInquiryAPI
    #         api = BankAPI.BalanceInquiryAPI(data=post_data)
    #         response = api.call()

    #         # Log the raw API response
    #         logger.debug(f"Raw API Response: {response.text}")

    #         # Attempt to parse JSON response
    #         try:
    #             response_data = response.json()
    #         except ValueError:
    #             logger.error("Invalid JSON response received.")
    #             return Response({"error": "Invalid JSON response from API."}, status=500)

    #         # Update the API being hit
    #         server_sync_object, created = BankServerSync.objects.get_or_create(api='BalanceInquiryAPI')
    #         server_sync_object.number_of_hits += 1
    #         server_sync_object.save()

    #         # Handle the API response
    #         if 200 <= response.status_code <= 299:
    #             decrypted_response = api.decrypt_response_data(method='Basic')
    #             logger.debug(f"Decrypted response: {decrypted_response}")

    #             if decrypted_response.get("RESPONSE") == "FAILURE":
    #                 logger.error("API response indicates failure.")
    #                 return Response(decrypted_response, status=500)
    #             else:
    #                 # Save the balance data to the database
    #                 balance_data = decrypted_response.get("balance", None)  # Extract the balance from the response
    #                 if balance_data:
    #                     # Save the balance data in the Balance model
    #                     balance_entry = Balance.objects.create(
    #                         client_name=client_name,
    #                         balance=balance_data,  # Assuming your model has a 'balance' field
    #                         last_updated=timezone.now()  # Add a timestamp
    #                     )
    #                     balance_entry.save()

    #                 # Update the last successful hit timestamp
    #                 server_sync_object.last_successful_hit = timezone.now()
    #                 server_sync_object.save()

    #                 decrypted_response['last_successful_hit'] = str(
    #                     timezone.localtime(server_sync_object.last_successful_hit)
    #                 )

    #                 return Response(decrypted_response)

    #         else:
    #             logger.error(f"API call returned non-success status: {response.status_code}")
    #             logger.error(f"API Error Response: {response.text}")  # Log the full error response
    #             return Response({"error": response_data, "message": "API returned an error."}, status=response.status_code)

    #     except requests.exceptions.RequestException as req_err:
    #         logger.error("Request failed: %s", str(req_err), exc_info=True)
    #         return Response({"error": "Request failed.", "details": str(req_err)}, status=500)

    #     except Exception as e:
    #         logger.error("Error in fetch_balance: %s", str(e), exc_info=True)
    #         return Response(
    #             {"error": str(e), "message": "Internal server error occurred."},
    #             status=500
    #         )