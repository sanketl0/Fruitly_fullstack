from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import base64


def main():
    response = "vewnSj5v+gLvTaAhb0JywLRfNcpuHv0Ks6hMmtyoXKZMCab/++nFhA1G4egmjX3w5kYtW2HP+abTwgbQLdsk6mH+GnCc4WxtU0CD+XRxZPmnkCA2Is0Owp60xRrz/uefaHWsl0sNqaub4Oi+4lMBSGCeCtTPZtkEpwloKjOVfwbOOYGa73Rd8ToPoLmHgC5VFlICKmLAFr+A4KW6jHVcTELMlfTHB5Lb5hMVbC7mv2G3XQp2sLGoYzRSutDdmvY9DSRF0t32wSpB8q0TLh7OpCfAkZ5pK2I3JOyLjpuQrGqzuh5tF8Wyicjo+9a4gIsS4dMFeDB/k2F4iwNDaPsrBapXKcycoC3ys0AVZAxWpMynVaFfBkxGUuqxMSrE4UGbAoeS0x18HrEwHI55y6JveM7Wyy7fOPXduP+d+Y6LkBoVmhVMYw9xztOpKp0LGgg5seiZf9K5mQTF/p9CJhqpidK/ez+LedfhM/7hPljAKf4jG6zfi0Kc265W8qWt/bsrbB7nra8vJl+n/N40ChL9RGvMmCFbe6DNNGVmPXTScr9j8ITCGDdoZc0/KYSFNYPflQ+0SDM+djo7reXtmHrVFVE0iQprdXN1b/HjNhNBAJONE/UkImkaxXLq7V0aMi7tyABffiovc9ru8Plr/GQxwzBU7aob0KwxuNVS1qlITRE="

    private_key_path = r"E:\CodeRizer_Work\Projects\FruitlyPayments\keys\privkey.pem"

    private_key = RSA.importKey(open(private_key_path).read())

    cipher = PKCS1_v1_5.new(private_key)
    encrypteddata = base64.b64decode(response)
    aes_key = cipher.decrypt(encrypteddata, None).decode()
    print(aes_key)


if __name__ == '__main__':
    main()
