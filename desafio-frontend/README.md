# Frontend - React + TypeScript + Vite

SPA para gerenciar carrinhos, consumindo a API FastAPI.

- Producao (Vercel): https://desafio-frontend-alpha.vercel.app
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

## Variaveis de ambiente
- `VITE_API_BASE` URL base da API
  - Desenvolvimento: `http://localhost:8000`
  - Producao (Vercel): `https://desafio-backend-cgfy.onrender.com`

## Scripts uteis
- `npm run dev` servidor de desenvolvimento (Vite)
- `npm run build` build de producao
- `npm run preview` pre-visualizacao do build

## Diferenciais
- Filtros no frontend: campos de User ID, Data inicial e Data final filtram a listagem (parametros enviados ao backend)

## Deploy na Vercel
1. No projeto da Vercel, adicione a variavel `VITE_API_BASE` (All Environments)
2. Faça um redeploy para aplicar

## Integracao com o backend
- As chamadas de API usam `VITE_API_BASE` (arquivo `src/api/carts.ts`)
- Endpoints esperados:
  - `GET /healthz`
  - `GET /carts`, `GET /carts/{id}`
  - `POST /carts`, `PUT /carts/{id}`, `DELETE /carts/{id}`
  - `POST /sync` (opcional para popular dados iniciais)

## Troubleshooting
- CORS bloqueado: garanta que o backend permita seu dominio (variavel `ALLOWED_ORIGINS` na Render). Para teste, use `*`.
- Lista vazia: rode `POST /sync` em `https://desafio-backend-cgfy.onrender.com/docs`.
- Base incorreta: confira `VITE_API_BASE` nas variaveis da Vercel e redeploy.

