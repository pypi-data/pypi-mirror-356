from devpayr.config.config import Config
from devpayr.exceptions.exceptions import DevPayrException


def test_valid_config_with_license():
    print("\n🧪 Testing valid config (license)...")
    config = Config({
        "license": "devpayr-test-key",
        "secret": "my-secret"
    })

    assert config.is_license_mode() is True
    assert config.is_api_key_mode() is False
    assert config.get("base_url") == "https://api.devpayr.com/api/v1/"
    assert config.get_auth_credential() == "devpayr-test-key"
    print("✅ Passed valid license config test!")


def test_valid_config_with_api_key():
    print("\n🧪 Testing valid config (api_key)...")
    config = Config({
        "api_key": "api-test-key",
        "secret": "my-secret"
    })

    assert config.is_license_mode() is False
    assert config.is_api_key_mode() is True
    assert config.get_auth_credential() == "api-test-key"
    print("✅ Passed valid API key config test!")


def test_missing_auth_key():
    print("\n🧪 Testing config with missing license/api_key...")
    try:
        Config({"secret": "something"})
    except DevPayrException as e:
        print("❌ Caught expected exception:", e)
        assert "license" in str(e) or "api_key" in str(e)
    else:
        raise AssertionError("Missing auth config should have raised DevPayrException")


def test_missing_secret():
    print("\n🧪 Testing config with missing secret...")
    try:
        Config({"license": "only-license-no-secret"})
    except DevPayrException as e:
        print("❌ Caught expected exception:", e)
        assert "secret" in str(e)
    else:
        raise AssertionError("Missing secret config should have raised DevPayrException")


if __name__ == "__main__":
    test_valid_config_with_license()
    test_valid_config_with_api_key()
    test_missing_auth_key()
    test_missing_secret()
