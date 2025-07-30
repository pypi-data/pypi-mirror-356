import os
import shutil
from devpayr.support.injectable_handler import InjectableHandler
from devpayr.crypto.crypto_helper import CryptoHelper
from devpayr.crypto.hash_helper import HashHelper


# Temporary folder to inject files into
TEST_DIR = "tests/tmp_injectables"
os.makedirs(TEST_DIR, exist_ok=True)

def make_injectable(slug, content, mode, secret, target_filename):
    encrypted = CryptoHelper.encrypt(content, secret)
    signature = HashHelper.signature(encrypted, secret)

    return {
        "slug": slug,
        "encrypted_content": encrypted,
        "signature": signature,
        "target_path": target_filename,
        "mode": mode
    }

def test_replace_mode():
    print("\n🧪 Testing 'replace' mode...")
    secret = "my-devpayr-secret"
    file_name = "replace_test.txt"
    full_path = os.path.join(TEST_DIR, file_name)

    injectable = make_injectable("test-replace", "First replace content", "replace", secret, file_name)

    InjectableHandler.process([injectable], {
        "secret": secret,
        "path": TEST_DIR,
        "verify": True
    })

    with open(full_path, "r", encoding="utf-8") as f:
        assert f.read() == "First replace content"
        print("✅ Replace mode passed.")


def test_append_mode():
    print("\n🧪 Testing 'append' mode...")
    secret = "my-devpayr-secret"
    file_name = "append_test.txt"
    full_path = os.path.join(TEST_DIR, file_name)

    # Start with base content
    with open(full_path, "w", encoding="utf-8") as f:
        f.write("Base")

    injectable = make_injectable("test-append", "Appended", "append", secret, file_name)

    InjectableHandler.process([injectable], {
        "secret": secret,
        "path": TEST_DIR
    })

    with open(full_path, "r", encoding="utf-8") as f:
        assert f.read() == "BaseAppended"
        print("✅ Append mode passed.")


def test_prepend_mode():
    print("\n🧪 Testing 'prepend' mode...")
    secret = "my-devpayr-secret"
    file_name = "prepend_test.txt"
    full_path = os.path.join(TEST_DIR, file_name)

    # Start with base content
    with open(full_path, "w", encoding="utf-8") as f:
        f.write("Base")

    injectable = make_injectable("test-prepend", "Prepended", "prepend", secret, file_name)

    InjectableHandler.process([injectable], {
        "secret": secret,
        "path": TEST_DIR
    })

    with open(full_path, "r", encoding="utf-8") as f:
        assert f.read() == "PrependedBase"
        print("✅ Prepend mode passed.")


def cleanup():
    shutil.rmtree(TEST_DIR)
    print("\n🧹 Cleaned up temporary test directory.")


if __name__ == "__main__":
    test_replace_mode()
    test_append_mode()
    test_prepend_mode()
    cleanup()
