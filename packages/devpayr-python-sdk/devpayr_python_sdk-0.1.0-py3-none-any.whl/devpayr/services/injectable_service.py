from devpayr.config.config import Config
from devpayr.http.http_client import HttpClient
from devpayr.exceptions.exceptions import DevPayrException


class InjectableService:
    """
    Manages injectables under a project — create, update, delete, stream (via license).
    """

    def __init__(self, config: Config):
        self.config = config
        self.http = HttpClient(config)

    def list(self, project_id: str | int) -> dict:
        """
        List all injectables for a project
        """
        return self.http.get(f"project/{project_id}/injectables")

    def create(self, project_id: str | int, data: dict) -> dict:
        """
        Create a new injectable (JSON or multipart)
        """
        return self.http.post(f"project/{project_id}/injectables", data)

    def show(self, project_id: str | int, injectable_id: str | int) -> dict:
        """
        Show a specific injectable
        """
        return self.http.get(f"project/{project_id}/injectables/{injectable_id}")

    def update(self, project_id: str | int, injectable_id: str | int, data: dict) -> dict:
        """
        Update an existing injectable
        """
        return self.http.put(f"project/{project_id}/injectables/{injectable_id}", data)

    def delete(self, project_id: str | int, injectable_id: str | int) -> dict:
        """
        Delete an injectable
        """
        return self.http.delete(f"project/{project_id}/injectables/{injectable_id}")

    def stream(self) -> dict:
        """
        Stream encrypted injectables using the license key
        """
        return self.http.get("injectable/stream")