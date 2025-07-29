from devpayr.crypto.crypto_helper import CryptoHelper
from devpayr.crypto.hash_helper import HashHelper


def test_crypto_helper():
    print("\n🔐 Testing CryptoHelper...")

    plaintext = "This is a secret message from DevPayr"
    key = "super-secret-key"

    encrypted = CryptoHelper.encrypt(plaintext, key)
    print(f"Encrypted: {encrypted}")

    decrypted = CryptoHelper.decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}")

    assert decrypted == plaintext
    print("✅ CryptoHelper test passed!")


def test_hash_helper():
    print("\n🔑 Testing HashHelper...")

    content = "Verify this payload"
    secret = "top-secret-signing-key"

    hash_value = HashHelper.hash(content)
    signature = HashHelper.signature(content, secret)

    print(f"Hash: {hash_value}")
    print(f"Signature: {signature}")

    assert HashHelper.verify_hash(content, hash_value)
    assert HashHelper.verify_signature(content, secret, signature)

    print("✅ HashHelper test passed!")


if __name__ == "__main__":
    test_crypto_helper()
    test_hash_helper()
