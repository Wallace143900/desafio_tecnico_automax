# Automax Cart API

Backend desenvolvido em **FastAPI** para gerenciar carrinhos de compras.  
O projeto utiliza **SQLAlchemy** para persistência em banco **SQLite** e segue boas práticas de desenvolvimento, incluindo **camada CRUD**, **schemas Pydantic**, **middleware global de erros** e tratamento de dados antigos.

---

## Funcionalidades

- Criar, listar e consultar carrinhos de compras.
- Armazenamento de produtos em formato JSON.
- Validação de dados com **Pydantic**.
- Tratamento de erros global com middleware.
- Compatibilidade com dados antigos (mapeia produtos com campos diferentes automaticamente).
- Possibilidade de integração com APIs externas (ex.: FakeStore API).

---

## Tecnologias

- **Python 3.11+**
- **FastAPI** – framework web
- **SQLAlchemy** – ORM para banco de dados
- **SQLite** – banco de dados leve
- **Pydantic** – validação e serialização de dados
- **Requests** – integração com APIs externas

---

---

## Endpoints principais

| Método | Rota            | Descrição                       |
|--------|----------------|--------------------------------|
| GET    | `/carts`       | Lista todos os carrinhos       |
| GET    | `/carts/{id}`  | Retorna um carrinho específico|
| POST   | `/carts`       | Cria um novo carrinho          |

### Exemplo de payload para POST /carts
```json
{
  "user_id": 1,
  "products": [
    {"productId": 400, "quantity": 201},
    {"productId": 401, "quantity": 500}
  ]
}

Tratamento de erros

{
  "status": "error",
  "message": "Ocorreu um erro interno no servidor.",
  "details": "mensagem do erro"
}