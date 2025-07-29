from devpayr.config.config import Config
from devpayr.http.http_client import HttpClient
from devpayr.exceptions.exceptions import DevPayrException


class LicenseService:
    """
    Manages licenses scoped to a specific project.
    """

    def __init__(self, config: Config):
        self.config = config
        self.http = HttpClient(config)

    def list(self, project_id: str | int) -> dict:
        """
        List all licenses for a given project
        """
        return self.http.get(f"project/{project_id}/licenses")

    def show(self, project_id: str | int, license_id: str | int) -> dict:
        """
        Get a specific license record
        """
        return self.http.get(f"project/{project_id}/licenses/{license_id}")

    def create(self, project_id: str | int, data: dict) -> dict:
        """
        Create a license under a project
        """
        return self.http.post(f"project/{project_id}/licenses", data)

    def revoke(self, project_id: str | int, license_id: str | int) -> dict:
        """
        Revoke a license
        """
        return self.http.post(f"project/{project_id}/licenses/{license_id}/revoke")

    def reactivate(self, project_id: str | int, license_id: str | int) -> dict:
        """
        Reactivate a revoked license
        """
        return self.http.post(f"project/{project_id}/licenses/{license_id}/reactivate")

    def delete(self, project_id: str | int, license_id: str | int) -> dict:
        """
        Delete a license
        """
        return self.http.delete(f"project/{project_id}/licenses/{license_id}")