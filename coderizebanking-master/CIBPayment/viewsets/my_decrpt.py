from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Random import get_random_bytes
import base64
import json
import logging

logger = logging.getLogger(__name__)

# Method to decrypt the encrypted data
def my_decrypt_response_data(encrypted_base64, private_key_file):
    try:
        # Decode the base64 encoded data
        encrypted_data = base64.b64decode(encrypted_base64)

        # Load the private key from the file
        with open(private_key_file, 'rb') as file:
            private_key = RSA.importKey(file.read())

        # Decrypt the data using the private key
        decrypter = PKCS1_v1_5.new(private_key)
        sentinel = get_random_bytes(16)  # Random bytes for error detection

        decrypted_data = decrypter.decrypt(encrypted_data, sentinel)

        if not decrypted_data:
            logger.error("Decryption returned empty data.")
            raise ValueError("Decryption failed due to empty data.")

        # Convert bytes back to JSON
        decrypted_payload = json.loads(decrypted_data.decode('UTF-8'))
        logger.debug("Decrypted Payload: %s", decrypted_payload)
        return decrypted_payload
    
    except Exception as e:
        logger.error("Decryption failed: %s", str(e), exc_info=True)
        raise ValueError(f"Decryption failed: {str(e)}")  # Raising error with more context
