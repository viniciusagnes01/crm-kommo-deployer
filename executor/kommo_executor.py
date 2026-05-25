import argparse
import json
import os
import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
sys.path.append(str(CURRENT_DIR))

from fields import create_missing_fields
from kommo_client import KommoClient
from pipeline import setup_pipeline
from tags import create_missing_tags



def load_env_file(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())

def load_config(config_path: str) -> dict:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de config nao encontrado: {config_path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    load_env_file()

    parser = argparse.ArgumentParser(description="Deploy automatico de estrutura base Kommo CRM - V4")
    parser.add_argument("--config", default=os.getenv("CONFIG_FILE", "config/cliente_config.example.json"))
    parser.add_argument("--apply", action="store_true", help="Aplica mudancas reais na conta Kommo")
    parser.add_argument("--dry-run", action="store_true", help="Simula o deploy sem alterar nada")
    args = parser.parse_args()

    dry_run = True
    if args.apply:
        dry_run = False
    if args.dry_run:
        dry_run = True

    subdomain = os.getenv("KOMMO_SUBDOMAIN", "").strip()
    api_token = os.getenv("KOMMO_API_TOKEN", "").strip()
    base_domain = os.getenv("KOMMO_BASE_DOMAIN", "kommo.com").strip()

    config = load_config(args.config)

    print("\n=== CRM Kommo Deployer - V4 ===")
    print(f"Cliente: {config.get('cliente', 'Sem nome')}")
    print(f"Config: {args.config}")
    print(f"Modo: {'DRY-RUN' if dry_run else 'APPLY REAL'}\n")

    if not dry_run:
        confirmation = input("Voce esta prestes a ALTERAR uma conta Kommo real. Digite APLICAR para continuar: ")
        if confirmation.strip() != "APLICAR":
            print("Execucao cancelada.")
            return

    client = KommoClient(
        subdomain=subdomain,
        api_token=api_token,
        base_domain=base_domain,
        dry_run=dry_run,
    )

    setup_pipeline(client, config)
    create_missing_fields(client, config)
    create_missing_tags(client, config)

    print("\nDeploy finalizado.")
    if dry_run:
        print("Nada foi alterado porque voce rodou em DRY-RUN.")
        print("Para aplicar de verdade, rode com: --apply")


if __name__ == "__main__":
    main()
