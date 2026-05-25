from typing import Any, Dict, List, Optional

from kommo_client import KommoClient


def _embedded_list(response: Dict[str, Any], key: str) -> List[Dict[str, Any]]:
    return response.get("_embedded", {}).get(key, []) or []


def find_field_by_name(client: KommoClient, name: str) -> Optional[Dict[str, Any]]:
    if client.dry_run:
        return None
    response = client.get("/leads/custom_fields")
    for field in _embedded_list(response, "custom_fields"):
        if field.get("name") == name:
            return field
    return None


def create_missing_fields(client: KommoClient, config: Dict[str, Any]) -> None:
    fields = config.get("campos_personalizados", [])
    sort = 100

    for field in fields:
        name = field["name"]
        field_type = field.get("type", "text")

        existing = find_field_by_name(client, name)
        if existing:
            print(f"[OK] Campo ja existe: {name}")
            continue

        payload = [{
            "name": name,
            "type": field_type,
            "sort": sort,
        }]

        client.post("/leads/custom_fields", payload)
        print(f"[OK] Campo criado: {name} ({field_type})")
        sort += 10
