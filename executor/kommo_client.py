import json
from typing import Any, Dict, List, Optional

import requests


class KommoApiError(RuntimeError):
    pass


class KommoClient:
    def __init__(self, subdomain: str, api_token: str, base_domain: str = "kommo.com", dry_run: bool = True) -> None:
        if not subdomain and not dry_run:
            raise ValueError("KOMMO_SUBDOMAIN nao foi informado.")
        if not api_token and not dry_run:
            raise ValueError("KOMMO_API_TOKEN nao foi informado.")

        subdomain = subdomain or "dry-run-subdomain"
        self.subdomain = subdomain.strip().replace("https://", "").replace("http://", "").split(".")[0]
        self.base_domain = base_domain.strip() or "kommo.com"
        self.dry_run = dry_run
        self.base_url = f"https://{self.subdomain}.{self.base_domain}/api/v4"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def request(
        self,
        method: str,
        path: str,
        payload: Optional[Any] = None,
        expected_statuses: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        expected_statuses = expected_statuses or [200, 201, 204]
        url = f"{self.base_url}{path}"

        if self.dry_run:
            print(f"[DRY-RUN] {method.upper()} {url}")
            if payload is not None:
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            return {"dry_run": True}

        response = requests.request(
            method=method.upper(),
            url=url,
            headers=self.headers,
            json=payload,
            timeout=30,
        )

        if response.status_code not in expected_statuses:
            raise KommoApiError(
                f"Erro Kommo API {response.status_code} em {method.upper()} {path}: {response.text}"
            )

        if response.status_code == 204 or not response.text:
            return {}

        try:
            return response.json()
        except ValueError:
            return {"raw": response.text}

    def get(self, path: str) -> Dict[str, Any]:
        return self.request("GET", path)

    def post(self, path: str, payload: Any) -> Dict[str, Any]:
        return self.request("POST", path, payload=payload)
