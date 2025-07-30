import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from dotenv import load_dotenv

load_dotenv()

def decrypt_ai_key(encrypted_base64_text: str) -> str:
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise ValueError("Missing SECRET_KEY in environment variables")

    # Decode base64
    encrypted_data = base64.b64decode(encrypted_base64_text)

    # Check "Salted__" header
    if encrypted_data[:8] != b'Salted__':
        raise ValueError("Invalid ciphertext format — missing Salted__ prefix")

    salt = encrypted_data[8:16]
    ciphertext = encrypted_data[16:]

    # EVP_BytesToKey key derivation (like OpenSSL)
    def evp_bytes_to_key(password, salt, key_len=32, iv_len=16):
        d = b''
        while len(d) < key_len + iv_len:
            d += hashlib.md5(d[-16:] + password + salt).digest()
        return d[:key_len], d[key_len:key_len + iv_len]

    key, iv = evp_bytes_to_key(secret_key.encode(), salt)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    try:
        return unpad(decrypted, AES.block_size).decode('utf-8')
    except ValueError as e:
        raise ValueError("Padding is incorrect. Decryption failed.") from e
