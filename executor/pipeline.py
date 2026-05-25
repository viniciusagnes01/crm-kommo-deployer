from typing import Any, Dict, List, Optional

from kommo_client import KommoClient


def _embedded_list(response: Dict[str, Any], key: str) -> List[Dict[str, Any]]:
    return response.get("_embedded", {}).get(key, []) or []


def find_pipeline_by_name(client: KommoClient, name: str) -> Optional[Dict[str, Any]]:
    if client.dry_run:
        return None
    response = client.get("/leads/pipelines")
    for pipeline in _embedded_list(response, "pipelines"):
        if pipeline.get("name") == name:
            return pipeline
    return None


def find_status_by_name(client: KommoClient, pipeline_id: int, name: str) -> Optional[Dict[str, Any]]:
    if client.dry_run:
        return None
    response = client.get(f"/leads/pipelines/{pipeline_id}/statuses")
    for status in _embedded_list(response, "statuses"):
        if status.get("name") == name:
            return status
    return None


def create_or_get_pipeline(client: KommoClient, config: Dict[str, Any]) -> Optional[int]:
    pipeline_name = config["pipeline"]["nome"]
    existing = find_pipeline_by_name(client, pipeline_name)
    if existing:
        print(f"[OK] Pipeline ja existe: {pipeline_name} (id={existing.get('id')})")
        return existing.get("id")

    payload = [{"name": pipeline_name}]
    response = client.post("/leads/pipelines", payload)

    if client.dry_run:
        print(f"[DRY-RUN] Criaria pipeline: {pipeline_name}")
        return 999999

    pipelines = _embedded_list(response, "pipelines")
    if not pipelines:
        raise RuntimeError("Pipeline criado, mas nao consegui localizar o ID na resposta da API.")

    pipeline_id = pipelines[0]["id"]
    print(f"[OK] Pipeline criado: {pipeline_name} (id={pipeline_id})")
    return pipeline_id


def create_missing_statuses(client: KommoClient, pipeline_id: int, config: Dict[str, Any]) -> None:
    etapas = config["pipeline"].get("etapas", [])
    sort = 10

    for etapa in etapas:
        existing = find_status_by_name(client, pipeline_id, etapa)
        if existing:
            print(f"[OK] Etapa ja existe: {etapa}")
            continue

        payload = [{"name": etapa, "sort": sort}]
        client.post(f"/leads/pipelines/{pipeline_id}/statuses", payload)
        print(f"[OK] Etapa criada: {etapa}")
        sort += 10


def setup_pipeline(client: KommoClient, config: Dict[str, Any]) -> Optional[int]:
    pipeline_id = create_or_get_pipeline(client, config)
    if pipeline_id is None:
        return None
    create_missing_statuses(client, pipeline_id, config)
    return pipeline_id
