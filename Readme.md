# Desafio Técnico Automax

Monorepo contendo o backend (FastAPI) e o frontend (React + Vite) do desafio. O backend está pronto para deploy gratuito na Render usando PostgreSQL; o frontend está pronto para deploy na Vercel.

- Backend (Render): https://desafio-backend-cgfy.onrender.com
- Frontend (Vercel): https://desafio-frontend-alpha.vercel.app

## Estrutura do projeto
- `desafio-backend/` — API FastAPI (código em `desafio-backend/app`)
- `desafio-frontend/` — SPA React + Vite
- `render.yaml` — Blueprint para criar o serviço Web e o banco Postgres Free na Render
- `desafio-backend/Procfile` — comando de start do Uvicorn
- `requirements.txt` — dependências do backend

## Rodando localmente
1) Backend
- Pré‑requisitos: Python 3.12+
- Passos:
  - Criar e ativar venv: `python -m venv .venv` e ativar (`. .venv/Scripts/activate` no Windows ou `. .venv/bin/activate` no Linux/Mac)
  - Instalar deps: `pip install -r requirements.txt`
  - Subir API: `cd desafio-backend && uvicorn app.main:app --reload --port 8000`
  - Docs: http://localhost:8000/docs

2) Frontend
- Pré‑requisitos: Node 18+
- Passos:
  - `cd desafio-frontend && npm install`
  - Criar arquivo `.env` com: `VITE_API_BASE=http://localhost:8000`
  - `npm run dev` e abrir http://localhost:5173

## Variáveis de ambiente
- Backend (Render)
  - `DATABASE_URL` — string do Postgres (use a Internal Database URL do banco da Render)
  - `ALLOWED_ORIGINS` — domínio(s) permitidos no CORS, separados por vírgula. Para liberar tudo: `*`
  - `PYTHON_VERSION` — `3.12.3` (opcional; já definido no blueprint)
- Frontend (Vercel)
  - `VITE_API_BASE` — base do backend, ex.: `https://desafio-backend-cgfy.onrender.com`

## Deploy
### Backend na Render (Blueprint)
1. Dashboard → New → Blueprint → selecione este repositório/branch
2. O `render.yaml` cria o Postgres Free e injeta `DATABASE_URL` automaticamente
3. `ALLOWED_ORIGINS` já vem como `*` (troque depois pelo domínio do Vercel)
4. Start do serviço: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend na Vercel
1. Defina `VITE_API_BASE` nas Environment Variables
2. Faça um redeploy para aplicar

## Endpoints principais (backend)
- `GET /healthz` — healthcheck
- `POST /sync` — importa carrinhos da Fake Store
- `GET /carts` — lista carrinhos
- `GET /carts/{id}` — detalhes
- `POST /carts` — cria
- `PUT /carts/{id}` — atualiza
- `DELETE /carts/{id}` — remove

## Dicas e troubleshooting
- CORS bloqueado: ajuste `ALLOWED_ORIGINS` no serviço da Render (sem barra final) ou use `*` para testes
- Serviço Free “acordando”: a primeira requisição pode demorar alguns segundos
- Sem dados? Rode `POST /sync` em `/docs`

## Licença
Uso livre para fins de avaliação técnica.
