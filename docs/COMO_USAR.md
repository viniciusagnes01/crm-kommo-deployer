# Como usar passo a passo

## Passo 1 - Abrir a pasta do projeto

Entre na pasta do projeto pelo terminal:

```bash
cd crm-kommo-deployer
```

## Passo 2 - Instalar dependencias

```bash
pip install -r requirements.txt
```

## Passo 3 - Criar arquivo .env

No Windows:

```bash
copy .env.example .env
```

Depois abra o arquivo `.env` e preencha:

```env
KOMMO_SUBDOMAIN=nome_do_subdominio
KOMMO_API_TOKEN=token_real_do_cliente
KOMMO_BASE_DOMAIN=kommo.com
CONFIG_FILE=config/cliente_config.example.json
```

## Passo 4 - Editar o JSON do cliente

Abra:

```text
config/cliente_config.example.json
```

Troque:

```json
"cliente": "NOME_DO_CLIENTE"
```

pelo nome real do cliente.

Ajuste etapas, campos e tags se necessario.

## Passo 5 - Rodar em modo seguro

```bash
python executor/kommo_executor.py --dry-run
```

Esse comando NAO muda nada no Kommo. Ele so mostra o que seria feito.

## Passo 6 - Aplicar no Kommo real

```bash
python executor/kommo_executor.py --apply
```

Quando pedir confirmacao, digite:

```text
APLICAR
```

## Passo 7 - Validar no Kommo

Confira:

- Pipeline criado
- Etapas criadas
- Campos criados
- Tags criadas
- Duplicidades
- Bot parado em Em Atendimento
- Follow-up configurado manualmente quando necessario
