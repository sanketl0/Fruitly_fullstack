from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.Random import get_random_bytes
import base64
import random


class SessionKey:

    def __init__(self, value=None):
        self.value = value
        self.encrypted_value = None

    def generate(self):
        self.value = get_random_bytes(16)
        return self.value

    def encrypt(self, public_key_path):
        with open(public_key_path, 'rb') as key_file:
                public_key = RSA.importKey(key_file.read())
        print(public_key)
        en = PKCS1_v1_5.new(public_key)
        encrypted_key = en.encrypt(self.value)

        self.encrypted_value = base64.b64encode(encrypted_key).decode('utf-8')
        return self.encrypted_value

    def decrypt(self, private_key_path):
        """Decrypt the encrypted session key using the RSA private key."""
        try:
            # Read the private key from the specified path
            with open(private_key_path, 'rb') as key_file:
                private_key = RSA.importKey(key_file.read())
        except FileNotFoundError:
            raise Exception(f"Private key file not found at {private_key_path}")

        # Decode the base64-encoded encrypted session key
        encrypted_data = base64.b64decode(self.encrypted_value)

        # Decrypt the session key using PKCS1_v1_5
        cipher = PKCS1_v1_5.new(private_key)
        decrypted_value = cipher.decrypt(encrypted_data, None)

        if decrypted_value is None:
            raise Exception("Decryption failed. The encrypted session key could not be decrypted.")

        self.value = decrypted_value
        return self.value



if __name__ == '__main__':
    # a = 'oG5mU1JJNBuwQaSLKb3wfRZks/cT2Vo2yBNNuqjNHDWEC144WxC8iKqBpJAgq7reFKC4sHNUmNPRDya1AvmQ7x1L+3EAdEs9FEWNurZuWTvZpk4y7JrGhg0rz9KptBf+JfJUkSMo7NR3Saxel6EYtckkDr3AGW7WJZmhcEoAMMXRws/hLVmaNHC/nOjCNqqBd4IOOAzdJh/HADRVI+YAJKT8dE4x9NTl+UX1zAooWhza+TsWEHfxzQIa7zai7WSa/wiJD3uD7mk5vT1WY/fKJBquCuzM7l35vigDhmb7dLVLuX8VMiNQrtErWNI0uVaag1jg+uZUtyDSxjPFi5yEpKVVc7+T503IDnCvkCFDygqasDsPL24qOjYk4XavTZvwGuPAdYNNkVnLzVElEhg4zS2ye+fa/8fZiMt/3fwYeN9dgn9i5R6VOFbXSuZJYPSci9k0oqz73h1nzFtps60rUEDoGIkGvm9waJU3W78VH5mIdGfGvvJjiKIuVHmi/huzEX9v4w3mW7RDGgmOuKImkqki+XWgyB0JvVmsLdO+cBaym/seZP3+zdfhO9AWSI2tDLD4Vf0jDjzoDSFN2mzUFgHK9mbtbXgvsnReoGqx/KsivzmZNLmDmtg8eR4Z9LnLni4rl4OtkDv5y/mxMtL3MBUUUajkw6OS6NnhEG895yo=',
    # s = SessionKey(a)
    sample_request = {'requestId': '',
                      'service': 'LOP',
                      'encryptedKey': 'oG5mU1JJNBuwQaSLKb3wfRZks/cT2Vo2yBNNuqjNHDWEC144WxC8iKqBpJAgq7reFKC4sHNUmNPRDya1AvmQ7x1L+3EAdEs9FEWNurZuWTvZpk4y7JrGhg0rz9KptBf+JfJUkSMo7NR3Saxel6EYtckkDr3AGW7WJZmhcEoAMMXRws/hLVmaNHC/nOjCNqqBd4IOOAzdJh/HADRVI+YAJKT8dE4x9NTl+UX1zAooWhza+TsWEHfxzQIa7zai7WSa/wiJD3uD7mk5vT1WY/fKJBquCuzM7l35vigDhmb7dLVLuX8VMiNQrtErWNI0uVaag1jg+uZUtyDSxjPFi5yEpKVVc7+T503IDnCvkCFDygqasDsPL24qOjYk4XavTZvwGuPAdYNNkVnLzVElEhg4zS2ye+fa/8fZiMt/3fwYeN9dgn9i5R6VOFbXSuZJYPSci9k0oqz73h1nzFtps60rUEDoGIkGvm9waJU3W78VH5mIdGfGvvJjiKIuVHmi/huzEX9v4w3mW7RDGgmOuKImkqki+XWgyB0JvVmsLdO+cBaym/seZP3+zdfhO9AWSI2tDLD4Vf0jDjzoDSFN2mzUFgHK9mbtbXgvsnReoGqx/KsivzmZNLmDmtg8eR4Z9LnLni4rl4OtkDv5y/mxMtL3MBUUUajkw6OS6NnhEG895yo=',
                      'oaepHashingAlgorithm': 'NONE',
                      'iv': '',
                      'encryptedData': 'wBJSefFsnJVlobh1cJR553w6Ay6b8/2frCjxvdZ1Bsnxztsul7Ha8lFl4PoZD+IhdlRShWdKgz3yJYIisGV/KKpyMSY3DILOpbkqEa0Qq0g=',
                      'clientInfo': '', 'optionalParam': ''}

    s = SessionKey()
    s.generate()

    s.encrypt(public_key_path=r'C:\Users\sanke\Desktop\payment\coderizebanking-master\keys\fruitly_public_key.txt')
    decrypted_value = s.decrypt(private_key_path=r"C:\Users\sanke\Desktop\payment\coderizebanking-master\keys\privkey.pem")
    
    print("Actual value: ", s.value)
    print("Encrypted value: ", s.encrypted_value)
    print("Decrypted Value: ", decrypted_value)

