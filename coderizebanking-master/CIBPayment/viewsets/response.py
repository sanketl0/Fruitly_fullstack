from ecdsa import SigningKey
from base64 import b64decode

def decrypt_with_ec_key(encrypted_data, private_key_path):
    try:
        # Load the EC private key
        with open(private_key_path, 'rb') as key_file:
            private_key = SigningKey.from_pem(key_file.read())

        # Decode the base64-encoded encrypted data
        encrypted_data = b64decode(encrypted_data)

        # EC decryption mechanism (if using the private key for decryption)
        decrypted_data = private_key.sign(encrypted_data)  # Sign instead of decrypt (depends on encryption)

        # Let's print the raw decrypted data as bytes first
        print("Decrypted Data (raw bytes):", decrypted_data)

        # If it's expected to be text (but encoded in a non-UTF-8 format), you can try decoding in other formats
        try:
            decrypted_text = decrypted_data.decode('utf-8')
            print("Decrypted Data (as UTF-8):", decrypted_text)
        except UnicodeDecodeError:
            print("Decryption output is not in UTF-8 format. It's likely binary or encoded.")

        return decrypted_data  # Returning raw decrypted data

    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

# Encrypted response and private key path
encrypted_response = b'nQM4RGMD1vtMbnhbrSqoDW8Z/jZRobD/DAQ8WejBM4Z1aLhQ2Zb3+axJj5DyyPQCk/LV0clRaXTnyXInD4Qxo+dSi7TIQs86DBaqINvaeA2BbDQcwq1lZMb5zX3wWmKHW/eZZjYxI4/C2yMDc6+kqXzZD0swx9rS29F6MVFFHibc/ITnlWg0TQEILcgrDuypHZz1zHqWNOBzYQc9xi7EEf+tENOAFQ29KUqVsmVDMuKPGft8gfu4C0VEWfhrS71se84zzXYhjqckWRqnW694P5Exzd6CO8OXPUcVoMtol58k68/RRDgBXdtjZs++P6LuFbsZXG42+d/4LCCeihlOINgqzoHcLXs6p1RUTYDYuLi/m5TbaUwQIeX2VL0s/zPkxo13CHNADIVWS8vf18MQF/hLQqHnrDU83Tr47iKLvmXYFUFAaVr0SQBzg6qyQAGhJgX8dyKuYMwU6euneUWkglD+UKKOmNnAN/pb+4mOx3HvMkFWjUDo/JsB0BVAWAlf6wpf1I4nowu4SKRoP5720dD+HRhQokUD8B+gnhAzSdcSsvM3yR1TA39dNRZ2s1LdM8caU0KujuDoVfvJmPEg/JpKBV9NGtdG0Gvht55yleo25WkJoZ6hTMkxqIP1crimZgPm/f451Y3p5c4MYJbAwbw0npYHR4phkoMzRyWwe2I='
private_key_file = r"C:/Users/sanke/Desktop/payment/coderizebanking-master/keys/privkey.pem"

# Decrypt the response
decrypted_output = decrypt_with_ec_key(encrypted_response, private_key_file)
print("Decrypted Response:", decrypted_output)
