# Automax Cart API (Backend)

API em FastAPI para cadastro, edicao, listagem e remocao de carrinhos. Pronta para deploy gratuito na Render usando PostgreSQL (via `DATABASE_URL`).

## Requisitos
- Python 3.12+

## Instalcao e execucao (dev)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: . .venv/bin/activate
pip install -r ../requirements.txt

cd desafio-backend
uvicorn app.main:app --reload --port 8000
```

Docs: http://localhost:8000/docs

## Variaveis de ambiente
- `DATABASE_URL` string do Postgres (Internal Database URL da Render). Se ausente, cai para SQLite local.
- `ALLOWED_ORIGINS` dominios permitidos no CORS, separados por virgula (ex.: `https://seu-site.vercel.app`) ou `*` para liberar tudo.
- `SYNC_INTERVAL_MINUTES` (opcional) intervalo em minutos para sincronizacao periodica.

## Rotas
- `GET /healthz` healthcheck
- `POST /sync` importa carrinhos da Fake Store
- `GET /carts` lista carrinhos
- `GET /carts/{id}` detalhes
- `POST /carts` cria
- `PUT /carts/{id}` atualiza
- `DELETE /carts/{id}` remove

## Diferenciais implementados
- Filtros de busca
  - `GET /carts` aceita `user_id`, `start_date` e `end_date` (ISO8601)
  - Exemplos:
    - `curl "http://localhost:8000/carts?user_id=5"`
    - `curl "http://localhost:8000/carts?start_date=2025-01-01T00:00:00Z&end_date=2025-01-31T23:59:59Z"`
- Scheduler opcional de sync
  - Ative com `SYNC_INTERVAL_MINUTES` (ex.: `60`) na Render
  - Observacao: no plano Free pode hibernar; para garantia use Cron Job externo chamando `POST /sync`
- Organizacao modular
  - `routers/`, `services.py`, `crud.py`, `models.py`, `schemas.py`, `errors/`

## Banco de dados
- ORM: SQLAlchemy 2.x
- Modelo: `Cart (id, user_id, date, products(JSON))`
- Tabelas criadas no startup (`Base.metadata.create_all`)

## Deploy na Render
### Blueprint (recomendado)
1. Render -> New -> Blueprint -> selecione o repo/branch
2. `render.yaml` cria Postgres Free e injeta `DATABASE_URL`
3. Ajuste `ALLOWED_ORIGINS` para o dominio do seu frontend
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Manual
1. Crie Postgres Free e copie a Internal Database URL
2. No servico Web, configure `DATABASE_URL`
3. Opcional: `ALLOWED_ORIGINS=*` para testes
4. Deploy

## Troubleshooting
- CORS: confira `ALLOWED_ORIGINS` (sem barra final)
- Free acordando: a primeira requisicao pode demorar
- Sem dados: rode `POST /sync` em `/docs`

