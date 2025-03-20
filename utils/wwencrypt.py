"""
Module File: wwencrypt.py
Description: This module contains the functions of RSA encryption for password.

Author: Icingworld
Date: 2025-03-20
Version: 0.1.0
"""

import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA

def rsa_psw(password: str, pub: str) -> str:
    """RSA encryption for password.

    :param password: password to be encrypted
    :param pub: public key
    :return: encrypted password
    """
    # load public key
    rsakey = RSA.importKey(pub)
    cipher = Cipher_pksc1_v1_5.new(rsakey)

    # encrypt password and return
    password_b64 = base64.b64encode(password.encode())
    cipher_text = base64.b64encode(cipher.encrypt(password_b64))
    return cipher_text.decode()
