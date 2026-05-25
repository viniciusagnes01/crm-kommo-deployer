# CRM Kommo Deployer

Pacote inicial para criar uma estrutura base de CRM Kommo no padrao V4.

Este projeto cria, via API do Kommo:

- Pipeline
- Etapas do funil
- Campos personalizados de lead
- Tags padrao

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
```

Onde alterar:

- `KOMMO_SUBDOMAIN`: subdominio da conta Kommo, sem https e sem .kommo.com.
- `KOMMO_API_TOKEN`: token real da API do cliente.
- `CONFIG_FILE`: caminho do JSON do cliente.

Nunca suba o arquivo `.env` real para o GitHub.

---

## 3. Testar sem alterar nada

Sempre rode primeiro em simulacao:

```bash
python executor/kommo_executor.py --dry-run
```

---

## 4. Aplicar de verdade

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

## 6. Fluxo operacional

1. Criar conta Kommo do cliente.
2. Gerar token API.
3. Criar JSON do cliente usando o template.
4. Rodar dry-run.
5. Conferir o que sera criado.
6. Rodar apply.
7. Validar no Kommo.
8. Configurar manualmente bot/WhatsApp conforme checklist.
