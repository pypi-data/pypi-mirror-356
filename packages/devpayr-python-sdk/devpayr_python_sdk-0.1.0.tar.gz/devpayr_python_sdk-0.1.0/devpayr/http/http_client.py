import requests
from devpayr.config.config import Config
from devpayr.exceptions.exceptions import DevPayrException
from devpayr.exceptions.exceptions import HttpRequestException
from devpayr.auth.api_key_auth import ApiKeyAuth
from devpayr.auth.license_auth import LicenseAuth


class HttpClient:
    """
    Handles authenticated HTTP requests to the DevPayr API using requests.
    """

    def __init__(self, config: Config):
        self.config = config
        self.base_url = config.get("base_url").rstrip("/") + "/"
        self.timeout = config.get("timeout", 10) / 1000  # convert ms to seconds

    def request(self, method: str, uri: str, options: dict = None) -> dict:
        options = options or {}
        headers = options.get("headers", {})
        query = options.get("query", {})
        json_data = options.get("json", {})
        multipart = options.get("multipart", None)

        # Accept JSON always
        headers["Accept"] = "application/json"

        # Content-Type if not multipart
        if method.upper() in ["POST", "PUT", "PATCH"] and not multipart:
            headers.setdefault("Content-Type", "application/json")

        # Inject auth headers
        if self.config.is_api_key_mode():
            headers.update(ApiKeyAuth.headers(self.config))

        if self.config.is_license_mode():
            headers.update(LicenseAuth.headers(self.config))

        # Inject global query params
        if self.config.get("injectables"):
            query["include"] = "injectables"

        if self.config.get("action"):
            query["action"] = self.config.get("action")

        if self.config.get("per_page"):
            query["per_page"] = self.config.get("per_page")

        try:
            response = requests.request(
                method=method.upper(),
                url=self.base_url + uri,
                headers=headers,
                params=query,
                json=json_data if not multipart else None,
                files=multipart,
                timeout=self.timeout,
            )

            if response.status_code >= 400:
                raise HttpRequestException(
                    response.status_code,
                    message=response.json().get("message", "API Request Failed")
                )

            try:
                return response.json()
            except Exception:
                raise DevPayrException("Invalid JSON response from DevPayr API.")

        except requests.exceptions.RequestException as e:
            raise DevPayrException(f"HTTP request failed: {str(e)}")

    def get(self, uri: str, query: dict = {}, extra: dict = {}) -> dict:
        return self.request("GET", uri, {**extra, "query": query})

    def post(self, uri: str, data: dict = {}, extra: dict = {}) -> dict:
        return self.request("POST", uri, {**extra, "json": data})

    def put(self, uri: str, data: dict = {}, extra: dict = {}) -> dict:
        return self.request("PUT", uri, {**extra, "json": data})

    def patch(self, uri: str, data: dict = {}, extra: dict = {}) -> dict:
        return self.request("PATCH", uri, {**extra, "json": data})

    def delete(self, uri: str, query: dict = {}, extra: dict = {}) -> dict:
        return self.request("DELETE", uri, {**extra, "query": query})
