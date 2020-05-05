import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



#A faire au tout début#
def create_key(password):
    password=password.encode()
    salt=""
    kdf= PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt.encode(),
                iterations=100000,
                backend=default_backend() ,
            )
    key=base64.urlsafe_b64encode(kdf.derive(password))
    Fernet_Key=Fernet(key)
    return Fernet_Key


def encrypt(Fernet_Key, message):
    return Fernet_Key.encrypt(message.encode())

def decrypt(Fernet_Key, message):
    try:
        data=Fernet_Key.decrypt(message)
        return data
    except:
        print("Tentative de décryptage échouée: Mauvais mot de passe")
