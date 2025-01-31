# import base64
# import json

# def try_base64_decode(data):
#     """Attempt to Base64 decode the given data."""
#     try:
#         decoded_data = base64.b64decode(data)
#         print("Base64 Decoded Data:", decoded_data)
#         return decoded_data
#     except Exception as e:
#         print(f"Error decoding Base64: {e}")
#         return None

# def print_hex_dump(data):
#     """Print a hex dump of the binary data."""
#     print("Hex Dump of Data:")
#     print(' '.join(f'{byte:02x}' for byte in data))

# def try_decode(data):
#     """Try decoding the data to UTF-8, if it fails, try Base64 decoding."""
#     # Ensure that data is in bytes format before attempting to decode
#     if isinstance(data, str):
#         data = data.encode('utf-8')  # Convert to bytes if it's a string
    
#     try:
#         decoded_data = data.decode('utf-8')  # Try to decode to UTF-8
#         print("Decoded Data:", decoded_data)
#         return decoded_data
#     except UnicodeDecodeError:
#         print("Decryption output is not in UTF-8 format. Trying Base64 decoding...")
#         decoded_base64_output = try_base64_decode(data)
#         return decoded_base64_output

# # Example of your decrypted data (replace this with the actual data you want to decode)
# decrypted_data = b'y\x9dy\xc6\xc6\x85\xea<\xf9\x81X#\xed\xdb\x1b{^j\xa7\x93J.\x14\xf1w\xa7\xf7\x00\nS\xdb\xa69\xf3Zh\xb6\xe6*-\x91\x8ay\xb1\xd0B\xcdr2\x8b1^\xd6GOJ\x984c:\xaa%r.'

# # Try decoding the decrypted data
# decoded_output = try_decode(decrypted_data)

# # If decoding fails, print the hex dump
# if not decoded_output:
#     print_hex_dump(decrypted_data)

# # Save binary data to a file
# with open('decrypted_output.bin', 'wb') as f:
#     f.write(decrypted_data)


import requests

url = "http://cib.localhost:8000/CIBPayment/Balance/Fetch/"
headers = {
    "Authorization": "Token d3a5c92915c184737a815e0092175cd331aa6ca5"
}
response = requests.get(url, headers=headers)

print(response.json())

