import os
import requests
from typing import Optional, Dict, Any

class GitHubProjectsAPI:
    """Simple wrapper for GitHub project management endpoints."""

    def __init__(self, token: Optional[str] = None, base_url: str = "https://api.github.com"):
        self.base_url = base_url.rstrip('/')
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.session = requests.Session()
        if self.token:
            self.session.headers.update({"Authorization": f"token {self.token}"})
        self.session.headers.update({"Accept": "application/vnd.github+json"})

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def list_org_projects(self, org: str, state: str = "open") -> Any:
        """List classic projects for an organization."""
        params = {"state": state}
        resp = self.session.get(self._url(f"/orgs/{org}/projects"), params=params)
        resp.raise_for_status()
        return resp.json()

    def create_org_project(self, org: str, name: str, body: str = "") -> Any:
        """Create a classic project for an organization."""
        payload = {"name": name, "body": body}
        resp = self.session.post(self._url(f"/orgs/{org}/projects"), json=payload)
        resp.raise_for_status()
        return resp.json()

    def list_user_projects(self, username: str, state: str = "open") -> Any:
        """List classic projects for a user."""
        params = {"state": state}
        resp = self.session.get(self._url(f"/users/{username}/projects"), params=params)
        resp.raise_for_status()
        return resp.json()
