from typing import Any, Callable, Dict, Optional
from devpayr.exceptions.exceptions import DevPayrException


class Config:
    """
    Configuration manager for DevPayr Python SDK.
    Accepts a user config dict, merges with defaults, and exposes utility getters.
    """

    required_keys = ["base_url", "secret"]

    defaults: Dict[str, Any] = {
        "base_url": "https://api.devpayr.com/api/v1/",
        "secret": None,
        "recheck": True,
        "injectables": True,
        "injectablesVerify": True,
        "injectablesPath": None,
        "invalidBehavior": "modal",  # Options: log | modal | redirect | silent
        "redirectUrl": None,
        "timeout": 1000,  # in milliseconds
        "action": "check_project",
        "onReady": None,  # Callable or None
        "handleInjectables": False,
        "injectablesProcessor": None,
        "customInvalidView": None,
        "customInvalidMessage": "This copy is not licensed for production use.",
        "license": None,
        "api_key": None,
        "per_page": None,
    }

    def __init__(self, user_config: Dict[str, Any]):
        self.config = {**self.defaults, **user_config}

        if not self.config.get("license") and not self.config.get("api_key"):
            raise DevPayrException('Either "license" or "api_key" must be provided in configuration.')

        for key in self.required_keys:
            if not self.config.get(key):
                raise DevPayrException(f'Missing required config field: "{key}"')

        # Normalize base_url to always end with a single slash
        self.config["base_url"] = self.config["base_url"].rstrip("/") + "/"

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def all(self) -> Dict[str, Any]:
        return self.config

    def is_enabled(self, key: str) -> bool:
        return bool(self.config.get(key))

    def is_license_mode(self) -> bool:
        return bool(self.config.get("license"))

    def is_api_key_mode(self) -> bool:
        return bool(self.config.get("api_key"))

    def get_auth_credential(self) -> str:
        return self.config.get("license") or self.config.get("api_key")

    def get_on_ready_callback(self) -> Optional[Callable]:
        return self.config.get("onReady")