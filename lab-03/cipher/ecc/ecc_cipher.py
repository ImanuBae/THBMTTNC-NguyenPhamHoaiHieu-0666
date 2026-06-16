import os

import ecdsa

KEY_DIR = os.path.join(os.path.dirname(__file__), 'keys')
PRIVATE_KEY_PATH = os.path.join(KEY_DIR, 'privateKey.pem')
PUBLIC_KEY_PATH = os.path.join(KEY_DIR, 'publicKey.pem')

if not os.path.exists(KEY_DIR):
    os.makedirs(KEY_DIR)


class ECCCipher:
    def __init__(self):
        pass

    def generate_keys(self):
        sk = ecdsa.SigningKey.generate()
        vk = sk.get_verifying_key()

        with open(PRIVATE_KEY_PATH, 'wb') as p:
            p.write(sk.to_pem())

        with open(PUBLIC_KEY_PATH, 'wb') as p:
            p.write(vk.to_pem())

    def load_keys(self):
        with open(PRIVATE_KEY_PATH, 'rb') as p:
            sk = ecdsa.SigningKey.from_pem(p.read())

        with open(PUBLIC_KEY_PATH, 'rb') as p:
            vk = ecdsa.VerifyingKey.from_pem(p.read())

        return sk, vk

    def sign(self, message, key):
        return key.sign(message.encode('ascii'))

    def verify(self, message, signature, key):
        try:
            return key.verify(signature, message.encode('ascii'))
        except ecdsa.BadSignatureError:
            return False
