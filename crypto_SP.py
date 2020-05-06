import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import datetime


#A faire au tout début: #
def create_key(password): #Fonction de création d'une clé de cryptage dérivée à partir du mot de passe du salon#
    password=password.encode()
    salt="" #Aucun salage car non nécessaire#
    kdf= PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32, #longueur de la clé#
                salt=salt.encode(),
                iterations=500000, #nombres d'itérations de la fonction d'hashage#
                backend=default_backend() ,
            )
    key=base64.urlsafe_b64encode(kdf.derive(password))
    Fernet_Key=Fernet(key)
    return Fernet_Key




#A faire à chaque fois qu'un message est envoié ou reçu#
def encrypt(Fernet_Key, message): #Encryptage du message à l'envoi#
    return Fernet_Key.encrypt(message.encode())

def decrypt(Fernet_Key, message): #Décryptage du message à la réception#
    try:
        data=Fernet_Key.decrypt(message)
        return data
    except:
        print("Tentative de décryptage échouée: Mauvais mot de passe")
