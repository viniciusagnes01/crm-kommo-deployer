import argparse
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.append(str(CURRENT_DIR))

from kommo_client import KommoClient
from kommo_executor import load_env_file
from sheets_webhook import lead_to_sheet_row, send_rows_to_sheets


def _extract_leads(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    embedded = response.get("_embedded") or {}
    return embedded.get("leads") or []


def fetch_leads(
    client: KommoClient,
    pipeline_id: Optional[int] = None,
    status_id: Optional[int] = None,
    limit: int = 250,
) -> List[Dict[str, Any]]:
    params = [f"limit={limit}", "with=contacts"]
    if pipeline_id is not None:
        params.append(f"filter[pipeline_id]={pipeline_id}")
    if status_id is not None:
        params.append(f"filter[statuses][0][status_id]={status_id}")

    path = f"/leads?{'&'.join(params)}"
    response = client.get(path)
    return _extract_leads(response)


def main() -> None:
    load_env_file()

    parser = argparse.ArgumentParser(description="Exporta leads do Kommo para uma planilha via webhook")
    parser.add_argument("--pipeline-id", type=int, default=None, help="Filtra leads por pipeline_id")
    parser.add_argument("--status-id", type=int, default=None, help="Filtra leads por status_id")
    parser.add_argument("--limit", type=int, default=250, help="Quantidade maxima de leads por chamada")
    parser.add_argument("--apply", action="store_true", help="Envia dados reais para a planilha")
    parser.add_argument("--dry-run", action="store_true", help="Simula a exportacao sem enviar dados")
    args = parser.parse_args()

    dry_run = True
    if args.apply:
        dry_run = False
    if args.dry_run:
        dry_run = True

    client = KommoClient(
        subdomain=os.getenv("KOMMO_SUBDOMAIN", "").strip(),
        api_token=os.getenv("KOMMO_API_TOKEN", "").strip(),
        base_domain=os.getenv("KOMMO_BASE_DOMAIN", "kommo.com").strip(),
        dry_run=dry_run,
    )

    leads = fetch_leads(
        client=client,
        pipeline_id=args.pipeline_id,
        status_id=args.status_id,
        limit=args.limit,
    )
    rows = [lead_to_sheet_row(lead) for lead in leads]

    print(f"Leads encontrados: {len(leads)}")
    send_rows_to_sheets(rows, dry_run=dry_run)

    if dry_run:
        print("Nada foi enviado porque voce rodou em DRY-RUN.")
        print("Para enviar de verdade, rode com: --apply")


if __name__ == "__main__":
    main()
