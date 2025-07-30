from devpayr.config.config import Config
from devpayr.http.http_client import HttpClient
from devpayr.exceptions.exceptions import DevPayrException


class ProjectService:
    """
    Handles DevPayr project-related operations:
    - create
    - update
    - delete
    - get
    - list
    """

    def __init__(self, config: Config):
        self.config = config
        self.http = HttpClient(config)

    def create(self, data: dict) -> dict:
        """
        Create a new project
        """
        return self.http.post("project", data)

    def update(self, project_id: str | int, data: dict) -> dict:
        """
        Update an existing project
        """
        return self.http.put(f"project/{project_id}", data)

    def delete(self, project_id: str | int) -> dict:
        """
        Delete a project
        """
        return self.http.delete(f"project/{project_id}")

    def get(self, project_id: str | int) -> dict:
        """
        Get a single project by ID
        """
        return self.http.get(f"project/{project_id}")

    def list(self) -> dict:
        """
        List all projects accessible by this API key or license
        """
        return self.http.get("projects")
