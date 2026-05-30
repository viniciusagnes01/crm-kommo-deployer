# CRM Kommo Deployer

Pacote inicial para criar uma estrutura base de CRM Kommo no padrao V4.

Este projeto cria, via API do Kommo:

- Pipeline
- Etapas do funil
- Campos personalizados de lead
- Tags padrao

Tambem inclui uma rotina de integracao para exportar leads do Kommo para uma planilha via webhook do Google Apps Script.

As automacoes de bot, mensagens e regras comerciais ficam documentadas no JSON como checklist/manual, porque a configuracao de Salesbot/WhatsApp pode variar conforme canal, permissao e conta.

---

## 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 2. Configurar acesso Kommo

Copie o arquivo `.env.example` para `.env`.

No Windows, voce pode copiar manualmente ou rodar:

```bash
copy .env.example .env
```

Depois edite o `.env`:

```env
KOMMO_SUBDOMAIN=insira_o_subdominio_aqui
KOMMO_API_TOKEN=insira_o_token_aqui
KOMMO_BASE_DOMAIN=kommo.com
CONFIG_FILE=config/cliente_config.example.json
SHEETS_WEBHOOK_URL=https://script.google.com/macros/s/SEU_WEBAPP_ID/exec
```

Onde alterar:

- `KOMMO_SUBDOMAIN`: subdominio da conta Kommo, sem https e sem .kommo.com.
- `KOMMO_API_TOKEN`: token real da API do cliente.
- `CONFIG_FILE`: caminho do JSON do cliente.
- `SHEETS_WEBHOOK_URL`: URL do Web App do Google Apps Script que grava na planilha.

Nunca suba o arquivo `.env` real para o GitHub.

---

## 3. Testar deploy do CRM sem alterar nada

Sempre rode primeiro em simulacao:

```bash
python executor/kommo_executor.py --dry-run
```

---

## 4. Aplicar deploy do CRM de verdade

Depois de conferir o dry-run:

```bash
python executor/kommo_executor.py --apply
```

O script vai pedir confirmacao. Digite:

```text
APLICAR
```

---

## 5. Criar JSON para um cliente novo

Copie:

```text
config/template_base.json
```

E crie um novo arquivo, por exemplo:

```text
config/multimed.json
```

Depois rode:

```bash
python executor/kommo_executor.py --config config/multimed.json --dry-run
python executor/kommo_executor.py --config config/multimed.json --apply
```

---

## 6. Integracao CRM e Planilha

A integracao usa um webhook do Google Apps Script para receber os leads em JSON e gravar as linhas na planilha.

### 6.1 Testar exportacao sem enviar para a planilha

```bash
python executor/export_leads_to_sheets.py --dry-run
```

Com filtros opcionais:

```bash
python executor/export_leads_to_sheets.py --pipeline-id 123456 --status-id 789012 --dry-run
```

### 6.2 Enviar leads para a planilha

Depois de configurar `SHEETS_WEBHOOK_URL` no `.env`:

```bash
python executor/export_leads_to_sheets.py --apply
```

### 6.3 Payload enviado para a planilha

O script envia:

```json
{
  "rows": [
    {
      "lead_id": 123,
      "nome": "Nome do lead",
      "preco": 0,
      "status_id": 111,
      "pipeline_id": 222,
      "responsavel_id": 333,
      "created_at": 1710000000,
      "updated_at": 1710000000,
      "Origem do Lead": "Meta Ads"
    }
  ]
}
```

Os campos personalizados do Kommo sao achatados automaticamente por nome do campo, como `Origem do Lead`, `UTM Campanha`, `Servico` e demais campos existentes no lead.

---

## 7. Fluxo operacional

1. Criar conta Kommo do cliente.
2. Gerar token API.
3. Criar JSON do cliente usando o template.
4. Rodar dry-run do deploy.
5. Conferir o que sera criado.
6. Rodar apply do deploy.
7. Validar no Kommo.
8. Configurar manualmente bot/WhatsApp conforme checklist.
9. Configurar `SHEETS_WEBHOOK_URL`.
10. Rodar dry-run da exportacao para planilha.
11. Rodar apply da exportacao para planilha.
