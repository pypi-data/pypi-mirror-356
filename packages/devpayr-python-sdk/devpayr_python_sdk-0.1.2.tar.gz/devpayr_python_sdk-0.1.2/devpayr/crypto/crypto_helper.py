import base64
import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from devpayr.exceptions.exceptions import CryptoException


class CryptoHelper:
    """
    Provides AES-256-CBC encryption and decryption using SHA-256 normalized key.
    Format: base64_encode(iv::ciphertext)
    """

    CIPHER_MODE = AES.MODE_CBC
    BLOCK_SIZE = 16  # AES block size

    @staticmethod
    def _normalize_key(key: str) -> bytes:
        return hashlib.sha256(key.encode()).digest()

    @staticmethod
    def encrypt(plaintext: str, key: str) -> str:
        try:
            normalized_key = CryptoHelper._normalize_key(key)
            iv = os.urandom(CryptoHelper.BLOCK_SIZE)
            cipher = AES.new(normalized_key, CryptoHelper.CIPHER_MODE, iv)
            encrypted_bytes = cipher.encrypt(pad(plaintext.encode(), CryptoHelper.BLOCK_SIZE))
            encoded = base64.b64encode(iv + b"::" + encrypted_bytes).decode()
            return encoded
        except Exception as e:
            raise CryptoException(f"Encryption failed: {str(e)}")

    @staticmethod
    def decrypt(encrypted: str, key: str) -> str:
        try:
            decoded = base64.b64decode(encrypted)
        except Exception:
            raise CryptoException("Failed to base64-decode encrypted string.")

        try:
            parts = decoded.split(b"::", 1)
            if len(parts) != 2:
                raise CryptoException("Invalid encrypted format — expected 'iv::cipherText'.")

            iv, ciphertext = parts
            normalized_key = CryptoHelper._normalize_key(key)
            cipher = AES.new(normalized_key, CryptoHelper.CIPHER_MODE, iv)
            decrypted = unpad(cipher.decrypt(ciphertext), CryptoHelper.BLOCK_SIZE)
            return decrypted.decode()
        except CryptoException:
            raise
        except Exception as e:
            raise CryptoException(f"Decryption failed: {str(e)}")
