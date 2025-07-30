from devpayr.config.config import Config
from devpayr.http.http_client import HttpClient
from devpayr.exceptions.exceptions import DevPayrException


class PaymentService:
    """
    Verifies if a project has an active payment/subscription using a license or API key.
    """

    def __init__(self, config: Config):
        self.config = config
        self.http = HttpClient(config)

    def check_with_api_key(self, project_id: str | int, query_params: dict = {}) -> dict:
        """
        Check payment status using a project-specific API key.
        """
        path = f"project/{project_id}/has-paid"
        return self.http.get(path, query_params)

    def check_with_license_key(self, query_params: dict = {}) -> dict:
        """
        Check payment status using a license key (license is in config).
        """
        path = "project/has-paid"
        payload = {
            "license": self.config.get("license"),
            "action": self.config.get("action"),
        }

        if self.config.get("injectables"):
            payload["include"] = "injectables"

        return self.http.post(path, payload | query_params)
