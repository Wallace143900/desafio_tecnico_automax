# Frontend — React + TypeScript + Vite

Aplicação SPA para gerenciar carrinhos, consumindo a API FastAPI.

- Produção (Vercel): https://desafio-frontend-alpha.vercel.app
- Backend (Render): https://desafio-backend-cgfy.onrender.com

## Requisitos
- Node.js 18+

## Rodando em desenvolvimento
```bash
cd desafio-frontend
npm install

# configure a base da API (dev)
echo VITE_API_BASE=http://localhost:8000 > .env

npm run dev
# abre em http://localhost:5173
```

## Variáveis de ambiente
- `VITE_API_BASE` — URL base da API
  - Desenvolvimento: `http://localhost:8000`
  - Produção (Vercel): `https://desafio-backend-cgfy.onrender.com`

## Scripts úteis
- `npm run dev` — servidor de desenvolvimento (Vite)
- `npm run build` — build de produção
- `npm run preview` — pré-visualização do build

## Deploy na Vercel
1. No projeto da Vercel, adicione a variável `VITE_API_BASE` (em All Environments)
2. Faça um redeploy para aplicar

## Integração com o backend
- As chamadas de API usam `VITE_API_BASE` (arquivo `src/api/carts.ts`)
- Endpoints esperados:
  - `GET /healthz`
  - `GET /carts`, `GET /carts/{id}`
  - `POST /carts`, `PUT /carts/{id}`, `DELETE /carts/{id}`
  - `POST /sync` (opcional para popular dados iniciais)

## Troubleshooting
- CORS bloqueado: garanta que o backend permita seu domínio (variável `ALLOWED_ORIGINS` na Render). Para teste, use `*`.
- Lista vazia: rode `POST /sync` em `https://desafio-backend-cgfy.onrender.com/docs`.
- Base incorreta: confira `VITE_API_BASE` nas variáveis da Vercel e redeploy.

