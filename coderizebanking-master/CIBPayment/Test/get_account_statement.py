import requests
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5


def main():
    # url = r"https://apibankingonesandbox.icicibank.com/api/Corporate/CIB/v1/AccountStatement"
    url = r"https://apibankingonesandbox.icicibank.com/api/Corporate/CIB/v1/TransactionInquiry"

    headers = {
        "accept": "*/*",
        "content-length": "684",
        "content-type": "text/plain",
        "APIKEY": "xYJgfFuYEf9W8hOYRSahL2t0T5y1s8lD"}

    data = {
        "AGGRID": "OTOE0480",
        "AGGRNAME": "FRUITLY",
        "CORPID": "CIBNEXT",
        "USERID": "CIBTESTING6",
        "URN": "SR213835043",
        "ACCOUNTNO": "000405001611",
        "FROMDATE": "01-01-2016",
        "TODATE": "30-12-2016",
    }

    data = {
        "AGGRID": "OTOE0480",
        "CORPID": "PRACHICIB1",
        "USERID": "USER3",
        "URN": "SR213835043",
        "UNIQUEID": "000451000301"
    }

    data = str(json.dumps(data)).encode('UTF-8')

    public_key_path = r"keys\ICICI_PUBLIC_CERT_UAT.txt"
    public_key = RSA.importKey(open(public_key_path, 'rb').read())

    encrypter = PKCS1_v1_5.new(public_key)
    encrypted_data = encrypter.encrypt(data)

    # data = """{ "data": """ +str(base64.b64encode(encrypted_data))+ "}"
    data = base64.b64encode(encrypted_data)

    print(data)

    r = requests.post(url=url, headers=headers, data=data)
    print(r.text)
    print(r.status_code)


if __name__ == '__main__':
    main()
