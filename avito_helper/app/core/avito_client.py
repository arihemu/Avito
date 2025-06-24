from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Dict

import requests
from requests import Response


class OAuthError(Exception):
    pass


def _current_time() -> int:
    return int(time.time())


@dataclass
class Token:
    access_token: str
    refresh_token: str
    expires_at: int

    @classmethod
    def from_response(cls, data: Dict[str, Any]) -> "Token":
        return cls(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_at=_current_time() + int(data.get("expires_in", 0)),
        )

    def is_expired(self) -> bool:
        return _current_time() >= self.expires_at


class AvitoClient:
    BASE_URL = "https://api.avito.ru"

    def __init__(self) -> None:
        self.client_id = os.getenv("AVITO_CLIENT_ID")
        self.client_secret = os.getenv("AVITO_CLIENT_SECRET")
        self.refresh_token = os.getenv("AVITO_REFRESH_TOKEN")
        self.token: Token | None = None

    def _auth_headers(self) -> Dict[str, str]:
        if not self.token or self.token.is_expired():
            self.refresh_access_token()
        assert self.token
        return {"Authorization": f"Bearer {self.token.access_token}"}

    def refresh_access_token(self) -> None:
        url = f"{self.BASE_URL}/token"
        resp = requests.post(
            url,
            data={
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
            },
        )
        if resp.status_code != 200:
            raise OAuthError(f"Failed to refresh token: {resp.text}")
        self.token = Token.from_response(resp.json())

    def get(self, endpoint: str, **kwargs: Any) -> Response:
        url = f"{self.BASE_URL}{endpoint}"
        headers = kwargs.pop("headers", {})
        headers.update(self._auth_headers())
        return requests.get(url, headers=headers, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> Response:
        url = f"{self.BASE_URL}{endpoint}"
        headers = kwargs.pop("headers", {})
        headers.update(self._auth_headers())
        return requests.post(url, headers=headers, **kwargs)
