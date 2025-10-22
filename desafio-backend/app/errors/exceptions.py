from fastapi import HTTPException


class CartNotFoundException(HTTPException):
    def __init__(self, cart_id: int):
        super().__init__(status_code=404,
                         detail=f"Carrinho {cart_id} não encontrado")
