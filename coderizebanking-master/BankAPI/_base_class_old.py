
import requests
import json
import base64
import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from Logger import logger
from Cryptography import EncryptedResponse
from Cryptography import get_private_key, KeyPaths


class APIBaseClass:
    """ This is the base class of all Bank APIs. Encrypting data is handeled over here """

    # if os.environ.get('LIFECYCLE') == 'LIVE':
    api_key = "8MxSAQDoUg1LcqW4Ro1dMESQXZXsP9gy" # Live
    

    #else:
        #api_key = "xYJgfFuYEf9W8hOYRSahL2t0T5y1s8lD" # UAT

    # The headers for all APIs will be same
    headers = {
        "accept": "*/*",
        "content-length": "684",
        "content-type": "text/plain",
        "APIKEY": api_key}

    def __init__(self, data):
        self.data = data
        self.response = None
        self.url = None

        if not isinstance(self.data, dict):
            raise Exception('Only dictionary is allowed as input for now.')


    def call(self):
        """ Call the API and get response """

        if self.url is None:
            raise Exception('No url is defined.')
        
         # Log headers and payload
        logger.debug(f"Headers: {self.headers}")
        logger.debug(f"Payload: {self.data}")
        print(self.data)


        data = str(json.dumps(self.data)).encode('UTF-8')
        logger.debug(f"Non-encrypted Data: {data}")
        logger.debug(f"headers: {self.headers}")

        # region Encrypt data
        public_key_path = KeyPaths.ICICIPublicKey #r"keys\ICICI_PUBLIC_CERT_UAT.txt"
        logger.debug(f"Using Key: {public_key_path}")
        # public_key = RSA.importKey(open(public_key_path, 'rb').read())
        with open(public_key_path, 'rb') as key_file:
            public_key = RSA.importKey(key_file.read())

        encrypter = PKCS1_v1_5.new(public_key)
        
        encrypted_data = encrypter.encrypt(data)
        data = base64.b64encode(encrypted_data)
        logger.debug(f"Encrypted dataaa: {data}")
        # endregion

        # region Call the actual API
        self.response = requests.post(url=self.url, headers=self.headers, data=data)
        logger.debug(f"Response data received: {self.response.text}")
        print("headderrrr",self.headers)
        print("headder response text",self.response.text)
        logger.debug(f"Response status code: {self.response.status_code}")
        # endregion

        return self.response




    def decrypt_response_data(self, method='Basic'):
        """Decrypt the received data."""
        if self.response is None:
            raise Exception("Please call the API first. Response is None.")

        if not (200 <= self.response.status_code <= 299):
            logger.error(
                f"Cannot decrypt response. Status code: {self.response.status_code}, "
                f"Response text: {self.response.text}"
            )
            return {
                "success": False,
                "errorcode": self.response.status_code,
                "errormessage": self.response.text,
            }
            

        try:
            if method == 'Basic':
                response_data = self.response.text
                logger.debug(f"Received encrypted response: {response_data}")
                encrypted_response = EncryptedResponse(response_data)
                decrypted_response = encrypted_response.decrypt(private_key_path=get_private_key(), method='Basic')
            elif method == 'Hybrid':
                response_data = self.response.json()
                print("____encrypted data____:",response_data)
                logger.debug(f"____Received encrypted response__: {response_data}")
                encrypted_response = EncryptedResponse(
                    encrypted_data=response_data['encryptedData'],
                    encrypted_key=response_data['encryptedKey']
                )
                decrypted_response = encrypted_response.decrypt(
                    private_key_path=get_private_key(), method='Hybrid'
                )
            else:
                raise ValueError("Only 'Basic' or 'Hybrid' methods are allowed.")

            logger.debug(f"Decrypted response: {decrypted_response}")
            return decrypted_response
        except Exception as e:
            logger.error(f"Error decrypting response: {e}")
            raise






































    # def decrypt_response_data(self, method='Basic'):
    #     """ To decrypt the received data """

    #     if self.response is None:
    #         raise Exception("Please call the API first. Response in None.")

    #     if 200 <= self.response.status_code <= 299:
    #         # For simple data decryption
    #         if method == 'Basic':
    #             response_data = self.response.text
    #             logger.debug(f"Recieved encrypted response: encrypted_data: {response_data}")
    #             encrypted_response = EncryptedResponse(response_data)
    #             logger.debug(f"Starting decryption: method=Basic")
    #             decrypted_response = encrypted_response.decrypt(private_key_path=get_private_key(), method='Basic')

    #         # For decrypting data using hyrid model
    #         elif method == 'Hybrid':
    #             response_data = self.response.json()
    #             logger.debug(f"""Recieved encrypted response: 
    #                                             encrypted_data: {response_data['encryptedData']} 
    #                                             encrypted_key: {response_data['encryptedKey']}""")
    #             encrypted_response = EncryptedResponse(encrypted_data=response_data['encryptedData'],
    #                                                    encrypted_key=response_data['encryptedKey'])

    #             logger.debug(f"Starting decryption: method=Hybrid")
    #             decrypted_response = encrypted_response.decrypt(private_key_path=get_private_key(), method='Hybrid')

    #         else:
    #             raise Exception("Only methods allowed: Basic, Hybrid ")

    #         logger.debug(f"Decrypted response: {decrypted_response}")
    #         return decrypted_response
    #     else:
    #         raise Exception("Cannot call decrypt, status code is not between 200 and 299")

    