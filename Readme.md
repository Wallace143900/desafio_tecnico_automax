# Desafio Tecnico Automax

Monorepo com backend (FastAPI) e frontend (React + Vite).

- Backend (Render): https://desafio-backend-cgfy.onrender.com
- Frontend (Vercel): https://desafio-frontend-alpha.vercel.app

## Estrutura
- `desafio-backend/` API FastAPI (codigo em `desafio-backend/app`)
- `desafio-frontend/` SPA React + Vite
- `render.yaml` Blueprint (servico Web + Postgres Free)
- `desafio-backend/Procfile` comando de start do Uvicorn
- `requirements.txt` dependencias do backend

## Rodando localmente
1) Backend
- Requisitos: Python 3.12+
- Passos:
  - `python -m venv .venv` e ativar (`. .venv/Scripts/activate` no Windows ou `. .venv/bin/activate` no Linux/Mac)
  - `pip install -r requirements.txt`
  - `cd desafio-backend && uvicorn app.main:app --reload --port 8000`
  - Docs: http://localhost:8000/docs

2) Frontend
- Requisitos: Node 18+
- Passos:
  - `cd desafio-frontend && npm install`
  - Criar `.env` com `VITE_API_BASE=http://localhost:8000`
  - `npm run dev` e abrir http://localhost:5173

## Variaveis de ambiente
- Backend (Render)
  - `DATABASE_URL` string do Postgres (Internal Database URL)
  - `ALLOWED_ORIGINS` dominios permitidos no CORS, separados por virgula. Para testes: `*`
  - `PYTHON_VERSION` por exemplo `3.12.3`
  - Opcional: `SYNC_INTERVAL_MINUTES` intervalo em minutos para sync periodico
- Frontend (Vercel)
  - `VITE_API_BASE` base do backend (ex.: `https://desafio-backend-cgfy.onrender.com`)

## Deploy
### Backend na Render (Blueprint)
1. Dashboard -> New -> Blueprint -> selecione este repo/branch
2. O `render.yaml` cria Postgres Free e injeta `DATABASE_URL`
3. `ALLOWED_ORIGINS` vem como `*` (troque depois pelo dominio do Vercel)
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend na Vercel
1. Defina `VITE_API_BASE` nas Environment Variables (All Environments)
2. Redeploy para aplicar

## Endpoints principais (backend)
- `GET /healthz` healthcheck
- `POST /sync` importa carrinhos da Fake Store
- `GET /carts` lista carrinhos (suporta filtros abaixo)
- `GET /carts/{id}` detalhes
- `POST /carts` cria
- `PUT /carts/{id}` atualiza
- `DELETE /carts/{id}` remove

## Diferenciais implementados
- Filtros de busca no backend e frontend
  - Query params em `GET /carts`: `user_id`, `start_date`, `end_date`
  - Exemplos:
    - `curl "https://desafio-backend-cgfy.onrender.com/carts?user_id=5"`
    - `curl "https://desafio-backend-cgfy.onrender.com/carts?start_date=2025-01-01T00:00:00Z&end_date=2025-01-31T23:59:59Z"`
  - No frontend, campos de filtro (User ID e intervalo de datas) foram adicionados
- Scheduler opcional de sincronizacao
  - Defina `SYNC_INTERVAL_MINUTES` no backend (Render) para executar o sync periodico
  - Ex.: `SYNC_INTERVAL_MINUTES=60`
  - Observacao: no plano Free a instancia pode hibernar; para garantia use Cron Job externo chamando `POST /sync`
- Organizacao modular do backend
  - Pastas/arquivos: `routers/`, `services.py`, `crud.py`, `models.py`, `schemas.py`, `errors/`
- Frontend em React (Vite)

## Troubleshooting
- CORS bloqueado: ajuste `ALLOWED_ORIGINS` (sem barra final) ou use `*` para testes
- Servico Free acordando: a primeira requisicao pode demorar
- Sem dados? Rode `POST /sync` em `/docs`

## Licenca
Uso livre para fins de avaliacao tecnica.

