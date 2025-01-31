import json
import base64

from .session_key import SessionKey
# from .data_to_encrypt import DataToEncrypt

import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


class DecryptedData:
    """ Decrypted response from CIB Payments API """

    def __init__(self, data=None):
        self.decrypted_data = data
        self.encrypted_data = None

    def __str__(self):
        return str(self.decrypted_data)

    def to_dict(self):
        """ Convert to dictionary from json"""
        return self.decrypted_data

    def encrypt_hybrid(self, public_key_path):
        # Generate random number and encrypt it using key
        session_key = SessionKey()
        session_key.generate()
        encryptedKey = session_key.encrypt(public_key_path=public_key_path)

        # Generate IV and encrypt it using key
        iv = SessionKey()
        iv.generate()
        iv.encrypt(public_key_path=public_key_path)

        # Encrypt the response data
        request_data = json.dumps(self.decrypted_data).encode('utf-8')
        cipher = AES.new(session_key.value, AES.MODE_CBC, iv=iv.value)

        encrypted_data = cipher.encrypt(pad(request_data, AES.block_size))
        encrypted_data = base64.b64encode(encrypted_data).decode('utf-8')

        # Fill all these values in response to return
        return_dict = dict()
        return_dict['encryptedKey'] = encryptedKey
        return_dict['encryptedData'] = encrypted_data
        return_dict['iv'] = base64.b64encode(iv.value).decode('utf-8')

        return return_dict
