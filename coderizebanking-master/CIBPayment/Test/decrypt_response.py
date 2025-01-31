
import json

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import base64


def decrypt_request(request_data):
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

    :param request:
    :return:
    """
    # Get the private key

    externKey = "E:\CodeRizer_Work\Projects\FruitlyPayments\keys\privkey.pem"

    # Read the private key
    priv_key = RSA.importKey(open(externKey).read())
    print("Key Imported")

    # Decode then decrypt the encryptedKey
    # Decrypted key is called SessionKey by ICICI
    cipher = PKCS1_v1_5.new(priv_key)
    encryptedKey = base64.b64decode(request_data['encryptedKey'])
    aes_key = cipher.decrypt(encryptedKey, None)
    print(f"Decrypted AES Key: {aes_key}")
    # Decode and decrypt encryptedData
    """
    Response = Base64Decode (AES/CBC/PKCS5PaddingDecryption(encryptedData,SessionKey, IV)) 
    """

    encryptedData = base64.b64decode(request_data['encryptedData'])
    print(f"Converted data from base 64: {encryptedData}")

    cipher = AES.new(aes_key, AES.MODE_CBC, iv=encryptedData[:16])
    response_json = json.loads(unpad(cipher.decrypt(encryptedData[16:]), 16))

    print(f"Decrypted Data: {response_json}")
    print(f"Decrypted Data Type: {type(response_json)}")

    return response_json

    # endregion


if __name__ == '__main__':
    sample_request = {"requestId": "", "service": "CIB", "oaepHashingAlgorithm": "NONE",
                      "encryptedKey": "c6DXp3vI6pOWLnnFuC9nFglYvkfwuUMuxDtxaxP45pUQ6vwg84TBF+9UotkJk+G6cf0vUxXHBy939nJniPB9RfLIHK/HGGkKdLm9HDCFiwFlYlga9C1Q62u7P5GzXv4cvQLE+Rs4hfu6OFn8LxlD705mkzoKKvknrOXTHZM1veDZ7c2BVSXCZiajRtfWNpu9PSU6CyGddHH4SglIC3P39nI80RicP5QaPcr8ymkmxXUBrLORas7x6AV48BJPn/VftFl//txvnro4cPAOBnGIIZSS5teAkhBZTE2ulP50Me7Wa7BWf8xveG5s9i2a/7ox5tICyoEMYCuwAUbbZsk3Aarixeyg/vCe8ux6IyL8QhoSDXCFJni3DRGjU857qLro9GlZRVbrSchJ60jICszUIWm/hht6M6OGu/DtaHz/20MmjUi+A7pt/u8Np//9KyfdiDBZSxJa7BUX7nZl5KUpywI/a9csR/M7H6GZdsUDy5G7wD8jR1lTzxJSDPriZNXnnROxaoDkwwRwcymn25Qi8/XPe+4TCX6sSH86i0fC7FlqjjyiENGWWX7IZKW/KkrywmVB8EF63+Oq0dAkb8MgCkCnEqSvZRyun06ZbP7FQAEkce9lIlY2t52QoCG7MwwoBji8iD9j6BVlHhNseetWvE1JoXgMFsd6HtjDReSlHF8=",
                      "encryptedData": "9JYaespt57tzp5xlp6V7CeENzg8nd3Mi3YUVCgqO1m1zp51qBwLFrPX56hR9KxLFZcZNbq1Gwrl4bSV9eikflxncXxAi+CAJh4Oi7w6S+yfhVkN1MsaG3WyFR/6YaYkp"}

    decrypt_request(sample_request)