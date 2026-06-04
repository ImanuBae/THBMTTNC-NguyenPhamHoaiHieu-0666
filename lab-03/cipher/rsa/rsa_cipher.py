import os

import rsa

KEY_DIR = os.path.join(os.path.dirname(__file__), 'key')
PUBLIC_KEY_PATH = os.path.join(KEY_DIR, 'public.pem')
PRIVATE_KEY_PATH = os.path.join(KEY_DIR, 'private.pem')

if not os.path.exists(KEY_DIR):
    os.makedirs(KEY_DIR)
    
class RSACipher:
    def __init__(self):
        pass
    def generate_key(self, bits=1024):
        (public_key, private_key) = rsa.newkeys(bits)
        with open(PUBLIC_KEY_PATH, 'wb') as p:
            p.write(public_key.save_pkcs1('PEM'))
        with open(PRIVATE_KEY_PATH, 'wb') as p:
            p.write(private_key.save_pkcs1('PEM'))
    
    def load_key(self):
        with open(PUBLIC_KEY_PATH, 'rb') as p:
            public_key = rsa.PublicKey.load_pkcs1(p.read())
        with open(PRIVATE_KEY_PATH, 'rb') as p:
            private_key = rsa.PrivateKey.load_pkcs1(p.read())
        return public_key, private_key
    
    def encrypt(self, message, key):
        return rsa.encrypt(message.encode('utf-8'), key)
    
    def decrypt(self, ciphertext, key):
        try:
            return rsa.decrypt(ciphertext, key).decode('utf-8')
        except Exception:
            return False
        
    def sign(self, message, key):
        return rsa.sign(message.encode('utf-8'), key, 'SHA-1')

    def verify(self, message, signature, key):
        try:
            rsa.verify(message.encode('utf-8'), signature, key)
            return True
        except Exception:
            return False
