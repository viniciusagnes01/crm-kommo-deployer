import os
from typing import Any, Dict, List

import requests


class SheetsWebhookError(RuntimeError):
    pass


def _flatten_custom_fields(lead: Dict[str, Any]) -> Dict[str, Any]:
    fields: Dict[str, Any] = {}
    for field in lead.get("custom_fields_values") or []:
        name = field.get("field_name") or str(field.get("field_id") or "campo_sem_nome")
        values = field.get("values") or []
        parsed_values: List[str] = []
        for value in values:
            raw = value.get("value") if isinstance(value, dict) else value
            if raw is not None:
                parsed_values.append(str(raw))
        fields[name] = ", ".join(parsed_values)
    return fields


def lead_to_sheet_row(lead: Dict[str, Any]) -> Dict[str, Any]:
    row = {
        "lead_id": lead.get("id"),
        "nome": lead.get("name"),
        "preco": lead.get("price"),
        "status_id": lead.get("status_id"),
        "pipeline_id": lead.get("pipeline_id"),
        "responsavel_id": lead.get("responsible_user_id"),
        "created_at": lead.get("created_at"),
        "updated_at": lead.get("updated_at"),
    }
    row.update(_flatten_custom_fields(lead))
    return row


def send_rows_to_sheets(rows: List[Dict[str, Any]], dry_run: bool = True) -> None:
    webhook_url = os.getenv("SHEETS_WEBHOOK_URL", "").strip()

    if not webhook_url and not dry_run:
        raise SheetsWebhookError("SHEETS_WEBHOOK_URL nao foi informado.")

    payload = {"rows": rows}

    if dry_run:
        print("[DRY-RUN] POST SHEETS_WEBHOOK_URL")
        print(payload)
        return

    response = requests.post(webhook_url, json=payload, timeout=30)
    if response.status_code >= 400:
        raise SheetsWebhookError(f"Erro ao enviar dados para planilha: {response.status_code} - {response.text}")
