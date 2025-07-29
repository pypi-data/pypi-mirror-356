from devpayr.config.config import Config
from devpayr.http.http_client import HttpClient
from devpayr.exceptions.exceptions import DevPayrException


class DomainService:
    """
    Manages domains tied to a project (whitelisted or license-bound).
    """

    def __init__(self, config: Config):
        self.config = config
        self.http = HttpClient(config)

    def list(self, project_id: str | int) -> dict:
        """
        List all domains under a project
        """
        return self.http.get(f"project/{project_id}/domains")

    def create(self, project_id: str | int, data: dict) -> dict:
        """
        Create a domain under a project
        """
        return self.http.post(f"project/{project_id}/domains", data)

    def show(self, project_id: str | int, domain_id: str | int) -> dict:
        """
        Show a specific domain entry
        """
        return self.http.get(f"project/{project_id}/domain/{domain_id}")

    def update(self, project_id: str | int, domain_id: str | int, data: dict) -> dict:
        """
        Update a domain record
        """
        return self.http.put(f"project/{project_id}/domain/{domain_id}", data)

    def delete(self, project_id: str | int, domain_id: str | int) -> dict:
        """
        Delete a domain record
        """
        return self.http.delete(f"project/{project_id}/domains/{domain_id}")