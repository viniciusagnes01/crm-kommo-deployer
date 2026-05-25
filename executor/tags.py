from typing import Any, Dict, List, Optional

from kommo_client import KommoClient


def _embedded_list(response: Dict[str, Any], key: str) -> List[Dict[str, Any]]:
    return response.get("_embedded", {}).get(key, []) or []


def find_tag_by_name(client: KommoClient, name: str) -> Optional[Dict[str, Any]]:
    if client.dry_run:
        return None
    response = client.get("/leads/tags")
    for tag in _embedded_list(response, "tags"):
        if tag.get("name") == name:
            return tag
    return None


def create_missing_tags(client: KommoClient, config: Dict[str, Any]) -> None:
    tags = config.get("tags_padrao", [])

    for tag_name in tags:
        existing = find_tag_by_name(client, tag_name)
        if existing:
            print(f"[OK] Tag ja existe: {tag_name}")
            continue

        payload = [{"name": tag_name}]
        client.post("/leads/tags", payload)
        print(f"[OK] Tag criada: {tag_name}")
