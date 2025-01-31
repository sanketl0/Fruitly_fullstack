from re import I
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
#
import base64
import json

import os
from .encrypted_data import BasicEncryptedData, HybridEncryptedData
# from decrypted_data import DecryptedData
from Logger import logger


# class EncryptedResponse:
#     """ Response returned from Bank API (CIB Payments) """

#     def __init__(self, encrypted_data=None, encrypted_key=None):
#         self.encrypted_data = encrypted_data
#         self.encrypted_key = encrypted_key

#         self.decrypted_data = None

#     def decrypt(self, private_key_path, method='Basic'):

#         if method == 'Basic':
#             encrypted_data = BasicEncryptedData(encrypted_data=self.encrypted_data)
#             decrypted_data = encrypted_data.decrypt(private_key_path=private_key_path).to_dict()
#             return decrypted_data

#         elif method == 'Hybrid':
#             encrypted_data = HybridEncryptedData(encrypted_key=self.encrypted_key, encrypted_data=self.encrypted_data)
#             decrypted_data = encrypted_data.decrypt(private_key_path=private_key_path).to_dict()
#             return decrypted_data

#             # """ Convert data to bytes and then decrypt using our private key """
#             # print(self.encrypted_data)
#             # encrypted_data = base64.b64decode(self.encrypted_data)
#             #
#             # print("Base 64 decoded data: ", encrypted_data)
#             # private_key = RSA.importKey(open(private_key_path).read())
#             #
#             # cipher = PKCS1_v1_5.new(private_key)
#             # self.decrypted_data = cipher.decrypt(encrypted_data, None).decode()
#             #
#             # # Return to a Decrypted Response object
#             # return DecryptedData(self.decrypted_data)

#         else:
#             raise Exception("Only method allowed are: Basic, Hybrid")


class EncryptedResponse:
    """ Response returned from Bank API (CIB Payments). """

    def __init__(self, encrypted_data=None, encrypted_key=None):
        if not encrypted_data:
            raise ValueError("Encrypted data must be provided.")
        self.encrypted_data = encrypted_data
        self.encrypted_key = encrypted_key
        self.decrypted_data = None
        print("__encrypted response file data received _:",self.encrypted_data)

    def decrypt(self, private_key_path, method='Basic'):
        """
        Decrypt the encrypted response data.

        :param private_key_path: Path to the private key file.
        :param method: Decryption method ('Basic' or 'Hybrid').
        :return: Decrypted data as a dictionary.
        """
        if not private_key_path or not os.path.exists(private_key_path):
            raise FileNotFoundError(f"Private key file not found at: {private_key_path}")

        try:
            if method == 'Basic':
                logger.debug(f"Starting decryption using Basic method.")
                encrypted_data = BasicEncryptedData(encrypted_data=self.encrypted_data)
                decrypted_data = encrypted_data.decrypt(private_key_path=private_key_path).to_dict()

            elif method == 'Hybrid':
                if not self.encrypted_key:
                    raise ValueError("Encrypted key is required for Hybrid decryption.")
                logger.debug(f"Starting decryption using Hybrid method.-{encrypted_data}")
                encrypted_data = HybridEncryptedData(
                    encrypted_key=self.encrypted_key,
                    encrypted_data=self.encrypted_data
                )
                decrypted_data = encrypted_data.decrypt(private_key_path=private_key_path).to_dict()

            else:
                raise ValueError("Only methods allowed are: Basic, Hybrid.")

            logger.debug(f"Decryption successful. Decrypted data: {decrypted_data}")
            return decrypted_data

        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise
