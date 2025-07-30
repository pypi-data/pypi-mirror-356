import os
from unittest.mock import patch
from devpayr.config.config import Config
from devpayr.runtime.validator import RuntimeValidator
from devpayr.crypto.crypto_helper import CryptoHelper
from devpayr.crypto.hash_helper import HashHelper


# Helper to generate a mock injectable
def mock_injectable(slug: str, content: str, secret: str, mode: str, path: str):
    encrypted = CryptoHelper.encrypt(content, secret)
    signature = HashHelper.signature(encrypted, secret)

    return {
        "slug": slug,
        "encrypted_content": encrypted,
        "signature": signature,
        "target_path": path,
        "mode": mode,
    }


def test_runtime_validator_validate_success():
    print("\n🧪 Running RuntimeValidator.validate() with mocks...")

    # Setup config
    secret = "devpayr-secret"
    test_file = "runtime_test.txt"
    test_dir = "tests/tmp_runtime"
    os.makedirs(test_dir, exist_ok=True)

    config = Config({
        "license": "test-license-key",
        "secret": secret,
        "injectables": True,
        "handleInjectables": True,
        "injectablesVerify": True,
        "injectablesPath": test_dir,
        "recheck": True  # force fresh check
    })

    # Prepare mock response
    injectables = [
        mock_injectable("example", "Injected Content", secret, "replace", test_file)
    ]

    mock_response = {
        "data": {
            "has_paid": True,
            "injectables": injectables
        }
    }

    # Patch PaymentService.check_with_license_key to return the mock
    with patch("devpayr.services.payment_service.PaymentService.check_with_license_key", return_value=mock_response):
        validator = RuntimeValidator(config)
        result = validator.validate()

        assert result["data"]["has_paid"] is True
        output_file = os.path.join(test_dir, test_file)
        assert os.path.exists(output_file)

        with open(output_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert content == "Injected Content"

        print("✅ RuntimeValidator passed and injectables written correctly.")

    # Clean up
    os.remove(os.path.join(test_dir, test_file))
    os.rmdir(test_dir)


if __name__ == "__main__":
    test_runtime_validator_validate_success()
