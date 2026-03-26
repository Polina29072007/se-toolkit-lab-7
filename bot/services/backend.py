# bot/services/backend.py
from typing import Any, Dict, List
import httpx


class BackendError(Exception):
    pass


class BackendClient:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.base_url = str(config["LMS_API_BASE_URL"]).rstrip("/")
        self.api_key = config["LMS_API_KEY"]

    def _client(self) -> httpx.Client:
        return httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=5.0,
        )

    def get_items(self) -> List[Dict[str, Any]]:
        try:
            with self._client() as client:
                resp = client.get("/items/")
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPError as e:
            raise BackendError(str(e)) from e

    def get_pass_rates(self, lab: str) -> List[Dict[str, Any]]:
        try:
            with self._client() as client:
                resp = client.get("/analytics/pass-rates", params={"lab": lab})
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPError as e:
            raise BackendError(str(e)) from e