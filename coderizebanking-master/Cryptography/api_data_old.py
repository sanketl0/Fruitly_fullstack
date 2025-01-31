import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

from .session_key import SessionKey
from .encrypted_data import HybridEncryptedData


class APIData:

    def __init__(self, data=None):
        self._data = data
        self.encrypted_data = None

        if not isinstance(self._data, dict):
            raise Exception("Only dictionaries are allowed as input")

    def encrypt(self, method, public_key_path, **kwargs):
        """
        :param method:
        :param public_key_path:
        :param kwargs: iv = 'Mixed' or None
        :return:
        """
        if method == 'Basic':
            raise Exception("Basic method is not implemented yet.")
        elif method == 'Hybrid':
            if kwargs.get('iv') == 'Mixed':
                return self.encrypt_hybrid_mixed(public_key_path)
            else:
                return self.encrypt_hybrid(public_key_path)
        else:
            raise Exception("Only methods allowed are Basic, Hybrid ")

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
        request_data = json.dumps(self._data).encode('utf-8')
        cipher = AES.new(session_key.value, AES.MODE_CBC, iv=iv.value)

        encrypted_data = cipher.encrypt(pad(request_data, AES.block_size))
        encrypted_data = base64.b64encode(encrypted_data).decode('utf-8')

        # Fill all these values in response to return
        return HybridEncryptedData(encrypted_key=encryptedKey, encrypted_data=encrypted_data,
                                   iv=base64.b64encode(iv.value).decode('utf-8'))

    def encrypt_hybrid_mixed(self, public_key_path):
        """ This function is same as above except that iv get appended in from of encrypted data """

        # Generate random number and encrypt it using key
        session_key = SessionKey()
        session_key.generate()
        encryptedKey = session_key.encrypt(public_key_path=public_key_path)

        # Generate IV and encrypt it using key
        iv = SessionKey()
        iv.generate()
        iv.encrypt(public_key_path=public_key_path)

        # Encrypt the response data
        request_data = json.dumps(self._data).encode('utf-8')
        cipher = AES.new(session_key.value, AES.MODE_CBC, iv=iv.value)

        encrypted_data = cipher.encrypt(pad(request_data, AES.block_size))

        # Add IV to the starting of encrypted_data
        enc = bytearray(iv.value)
        enc.extend(encrypted_data)

        encrypted_data = base64.b64encode(enc).decode('utf-8')

        # Fill all these values in response to return
        return HybridEncryptedData(encrypted_key=encryptedKey, encrypted_data=encrypted_data)
