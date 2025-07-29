import os
from devpayr.config.config import Config
from devpayr.runtime.validator import RuntimeValidator
from devpayr.crypto.crypto_helper import CryptoHelper
from devpayr.crypto.hash_helper import HashHelper
from devpayr.contracts.injectable_processor import InjectableProcessorInterface
from devpayr.support.injectable_handler import InjectableHandler
from unittest.mock import patch


# 🔧 Custom injectable processor that uppercases the content before saving
class CustomProcessor(InjectableProcessorInterface):
    @staticmethod
    def handle(injectable: dict, secret: str, base_path: str, verify_signature: bool = True) -> str:
        slug = injectable.get("slug")
        encrypted = injectable.get("encrypted_content") or injectable.get("content")
        target_path = injectable.get("target_path")
        mode = injectable.get("mode", "replace")

        decrypted = CryptoHelper.decrypt(encrypted, secret).upper()  # Custom logic: uppercase content

        full_path = os.path.abspath(os.path.join(base_path, target_path))

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(decrypted)

        return full_path


def test_custom_processor_handling():
    print("\n🧪 Testing custom injectable processor...")

    # Setup
    secret = "custom-secret"
    test_file = "custom_test.txt"
    test_dir = "tests/tmp_custom"
    os.makedirs(test_dir, exist_ok=True)

    # Set custom processor
    InjectableHandler.set_processor(CustomProcessor)

    # Build mock injectable
    original = "Injected with style"
    encrypted = CryptoHelper.encrypt(original, secret)
    signature = HashHelper.signature(encrypted, secret)

    injectable = {
        "slug": "custom",
        "encrypted_content": encrypted,
        "signature": signature,
        "target_path": test_file,
        "mode": "replace"
    }

    mock_response = {
        "data": {
            "has_paid": True,
            "injectables": [injectable]
        }
    }

    config = Config({
        "license": "any-license",
        "secret": secret,
        "injectables": True,
        "handleInjectables": True,
        "injectablesPath": test_dir,
        "injectablesProcessor": CustomProcessor,
        "recheck": True
    })

    with patch("devpayr.services.payment_service.PaymentService.check_with_license_key", return_value=mock_response):
        validator = RuntimeValidator(config)
        result = validator.validate()

        # Assert file exists and content is uppercased
        target_path = os.path.join(test_dir, test_file)
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert content == original.upper()

        print("✅ Custom processor ran successfully and transformed content.")

    # Cleanup
    os.remove(target_path)
    os.rmdir(test_dir)


if __name__ == "__main__":
    test_custom_processor_handling()
