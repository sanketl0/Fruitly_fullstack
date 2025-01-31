import os
from pathlib import Path


def get_private_key():
    import os
    from Logger import logger
    possible_paths = [
        os.path.join(Path(__file__).parent.parent, 'keys', 'privkey.pem')
    ]
    for possible_path in possible_paths:
        if os.path.exists(possible_path):
            return possible_path

    logger.error("Private Key not found.")
    raise Exception("Private key not found")


class KeyPaths:
    # if os.environ.get('LIFECYCLE') == 'LIVE':
    ICICIPublicKey = os.path.join(
        Path(__file__).parent.parent, 'keys', 'ICICI_PUBLIC_CERT_PROD.txt')
    ICICIPublicKeyECollection = os.path.join(
        Path(__file__).parent.parent, 'keys', 'ICICI Live Cert.txt')

    # else:
    #     ICICIPublicKeyECollection = ICICIPublicKey = os.path.join(
    #         Path(__file__).parent.parent, 'keys', 'ICICI_PUBLIC_CERT_UAT.txt')

    FruitlyPublicKey = os.path.join(
        Path(__file__).parent.parent, 'keys', 'fruitly_public_key.txt')
    PrivateKey = get_private_key()


def get_icici_public_key():
    return KeyPaths.ICICIPublicKey


def get_fruitly_public_key():
    return KeyPaths.FruitlyPublicKey
