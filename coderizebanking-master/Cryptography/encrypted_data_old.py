import json

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import base64

from .decrypted_data import DecryptedData
from Crypto.Random import get_random_bytes

class BasicEncryptedData:
    def __init__(self, encrypted_data):
        self.encrypted_data = encrypted_data
        self.decrypted_data = None

    def decrypt(self, private_key_path):
        try:
            # Decode base64 encrypted data
            encrypted_data = base64.b64decode(self.encrypted_data)
            print("Base 64 decoded data:", encrypted_data)

            # Load private key
            with open(private_key_path, "rb") as key_file:
                private_key = RSA.importKey(key_file.read())

            # Decrypt the data
            cipher = PKCS1_v1_5.new(private_key)
            sentinel = get_random_bytes(16)  # Random sentinel used for decryption (required for PKCS1_v1_5)
            decrypted_data = cipher.decrypt(encrypted_data, sentinel)

            if not decrypted_data:
                raise ValueError("Decryption failed! The data could not be decrypted.")

            print("Decrypted data (raw):", decrypted_data)

            # Try decoding the decrypted data if it's UTF-8 encoded
            try:
                self.decrypted_data = json.loads(decrypted_data.decode('utf-8'))
                print("Decrypted Data:", self.decrypted_data)
            except UnicodeDecodeError:
                print("The decrypted data is not UTF-8 encoded, and may not be a JSON string.")
                print(decrypted_data)  # You can log or process the raw binary data if needed

            return DecryptedData(self.decrypted_data)

        except FileNotFoundError:
            raise FileNotFoundError(f"Private key file not found at: {private_key_path}")
        except ValueError as e:
            raise ValueError(f"Decryption error: {str(e)}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")


    




class HybridEncryptedData:

    def __init__(self, encrypted_key, encrypted_data, iv=None):
        self.encrypted_key = encrypted_key
        self.encrypted_data = encrypted_data
        self.iv = iv

        self.decrypted_data = None

    def decrypt(self, private_key_path):
        # region Decryption
        """
        IV= getFirst16Bytes(Base64Decode(encryptedData)
        SessionKey = Base64Decode(RSA/ECB/PKCS1Decryption(encryptedKey,ClientPrivateKey.p12,))
        # Session key is nothing but randomly generated string of length 16 (OR 32) .
        Response = Base64Decode (AES/CBC/PKCS5PaddingDecryption(encryptedData,SessionKey, IV))

        1. Get the IV- Base64 decode the encryptedData and get first 16 bytes and rest is
        encryptedResponse.
        bytes[] IV= getFirst16Bytes(Base64Decode(encryptedData)
        2. Decrypt encryptedKey using algo (RSA/ECB/PKCS1Padding) and Client’s private key.
        sessionKey = B64Decode(RSA/ECB/PKCS1Decryption(encryptedKey,ClientPrivateKey.p12,))
        3. Decrypt the response using algo AES/CBC/PKCS5Padding.
        Response = Base64Decode (AES/CBC/PKCS5Padding Decryption(encryptedData,SessionKey, IV))
        4. You need to skip first 16 bytes of response, as it contains IV.

        """

        # Read the private key
        private_key = RSA.importKey(open(private_key_path).read())

        # Decode then decrypt the encryptedKey
        # Decrypted key is called SessionKey by ICICI
        cipher = PKCS1_v1_5.new(private_key)
        encrypted_key = base64.b64decode(self.encrypted_key)
        aes_key = cipher.decrypt(encrypted_key, None)

        print(f"Decrypted AES Key: {aes_key}")
        # Decode and decrypt encryptedData

        encrypted_data = base64.b64decode(self.encrypted_data)
        print(f"Converted data from base 64: {encrypted_data}")

        cipher = AES.new(aes_key, AES.MODE_CBC, iv=encrypted_data[:16])

        self.decrypted_data = unpad(cipher.decrypt(encrypted_data[16:]), 16)
        return DecryptedData(self.decrypted_data)
        # response_json = json.loads()

        # print(f"Decrypted Data: {response_json}")
        # print(f"Decrypted Data Type: {type(response_json)}")
        #
        # self.decrypted_data = response_json
        # return response_json

        # endregion

    def to_dict(self):
        return_dict = dict()
        return_dict['encryptedKey'] = self.encrypted_key
        return_dict['encryptedData'] = self.encrypted_data
        return_dict['iv'] = self.iv
        return return_dict


if __name__ == '__main__':
    # sample_request = {"requestId": "", "service": "CIB", "oaepHashingAlgorithm": "NONE",
    #                   "encryptedKey": "c6DXp3vI6pOWLnnFuC9nFglYvkfwuUMuxDtxaxP45pUQ6vwg84TBF+9UotkJk+G6cf0vUxXHBy939nJniPB9RfLIHK/HGGkKdLm9HDCFiwFlYlga9C1Q62u7P5GzXv4cvQLE+Rs4hfu6OFn8LxlD705mkzoKKvknrOXTHZM1veDZ7c2BVSXCZiajRtfWNpu9PSU6CyGddHH4SglIC3P39nI80RicP5QaPcr8ymkmxXUBrLORas7x6AV48BJPn/VftFl//txvnro4cPAOBnGIIZSS5teAkhBZTE2ulP50Me7Wa7BWf8xveG5s9i2a/7ox5tICyoEMYCuwAUbbZsk3Aarixeyg/vCe8ux6IyL8QhoSDXCFJni3DRGjU857qLro9GlZRVbrSchJ60jICszUIWm/hht6M6OGu/DtaHz/20MmjUi+A7pt/u8Np//9KyfdiDBZSxJa7BUX7nZl5KUpywI/a9csR/M7H6GZdsUDy5G7wD8jR1lTzxJSDPriZNXnnROxaoDkwwRwcymn25Qi8/XPe+4TCX6sSH86i0fC7FlqjjyiENGWWX7IZKW/KkrywmVB8EF63+Oq0dAkb8MgCkCnEqSvZRyun06ZbP7FQAEkce9lIlY2t52QoCG7MwwoBji8iD9j6BVlHhNseetWvE1JoXgMFsd6HtjDReSlHF8=",
    #                   "encryptedData": "9JYaespt57tzp5xlp6V7CeENzg8nd3Mi3YUVCgqO1m1zp51qBwLFrPX56hR9KxLFZcZNbq1Gwrl4bSV9eikflxncXxAi+CAJh4Oi7w6S+yfhVkN1MsaG3WyFR/6YaYkp"}

    # encrypted_data = BasicEncryptedData(encrypted_key=sample_request['encryptedKey'],
    #                                      encrypted_data=sample_request['encryptedData'])

    # externKey = r"C:\Users\sanke\Desktop\payment\coderizebanking-master\keys\privkey.pem"

    # decrypted_data = encrypted_data.decrypt(private_key_path=externKey)

    # print(decrypted_data.to_dict())

    data = "G5uaXjFWeKxLQ3BVmnQr72RIUPg8gkPIYlV4el04ZeqOzKukrxsF8iaa5RVYps3K31JJFkmnJOsQiaGbzj98lDU2PSgtANt3/YlGqqoHzdwnPMCLdjbuVsJw6iQ4JQ5jfkdAlho3vO58AYBfIq9S1mJljTTgTgqxYEbBKOYv8Kq0OxmVrmWzuA9jDOmXOc91919Gdh2pyJac0PWNzLvLvDgAHQ1cqnHJbMvuuCQVFs2OHtZkAuS2mkZRpX+eBTJHavk7Qu6n4osRT/2M1nnP5jbO59pUck429DIPKUhg9lVOQdjxwY9TsDVKk/DqZOzna8Qq0XO9pQadQvK+bwwLZ0ue6JbQlSDbqhW4wDfMfxJgFQuBKKpNqSQIgS3ORzyFwoiUCoGDBxwrT0Okh7hanRR03to9pYgaSIw9w1BBFS9ur+54/B+QtnUJdcS4Xeu6EF+aT+oyjQVslcqvUBwAzUXzm8kBao7+OEl8JvUDE+ddVBOok5VtQ4PKLHPJQzk3u68UaGOpKarmLnCK1R0pHpXKhDyPbwE2HQH7NblMbsy3O4RkDZrKlgsTzhC/h1GGqKR56WDrhvRISishcymoUP+2QBLFe7jp+rkK4361F3mbqX7KEcOGQ66lrsjmy1vs7Dc+Oes75LuyBKAFxE2CEK+Gcqq+EHQq5tduN1wSiCA="
    
    enc = BasicEncryptedData(data)
    private_key_path = r"C:\Users\sanke\Desktop\payment\coderizebanking-master\keys\privkey.pem"
    
    dec = enc.decrypt(private_key_path)
    print("no data",dec)
