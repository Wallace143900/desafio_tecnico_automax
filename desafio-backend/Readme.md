# Automax Cart API (Backend)

API em FastAPI para cadastro, edição, listagem e remoção de carrinhos. Pronta para deploy gratuito na Render usando PostgreSQL (via `DATABASE_URL`).

## Requisitos
- Python 3.12+

## Instalação e execução (dev)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac: . .venv/bin/activate
pip install -r ../requirements.txt

cd desafio-backend
uvicorn app.main:app --reload --port 8000
```

Docs: http://localhost:8000/docs

## Variáveis de ambiente
- `DATABASE_URL` — string do Postgres (ex.: Internal Database URL da Render). Se ausente, cai para SQLite local.
- `ALLOWED_ORIGINS` — lista separada por vírgula com domínios permitidos no CORS (ex.: `https://seu-site.vercel.app`) ou `*` para liberar tudo.

## Rotas
- `GET /healthz` — healthcheck
- `POST /sync` — importa carrinhos da Fake Store
- `GET /carts` — lista carrinhos
- `GET /carts/{id}` — detalhes
- `POST /carts` — cria
- `PUT /carts/{id}` — atualiza
- `DELETE /carts/{id}` — remove

## Banco de dados
- ORM: SQLAlchemy 2.x
- Modelo principal: `Cart (id, user_id, date, products(JSON))`
- Tabelas criadas automaticamente no startup (`Base.metadata.create_all`)

## Deploy na Render
### Usando Blueprint (recomendado)
1. Render → New → Blueprint → selecione o repo/branch
2. O `render.yaml` cria Postgres Free e injeta `DATABASE_URL`
3. Ajuste `ALLOWED_ORIGINS` para o domínio do seu frontend
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Manual
1. Crie o banco Postgres Free e copie a Internal Database URL
2. No serviço Web, configure `DATABASE_URL` com essa URL
3. Opcional: `ALLOWED_ORIGINS=*` para testes
4. Deploy

## Troubleshooting
- CORS bloqueado: confira `ALLOWED_ORIGINS` (sem barra no final)
- Serviço Free “acordando”: a primeira requisição pode demorar
- Sem dados? Rode `POST /sync` em `/docs`

