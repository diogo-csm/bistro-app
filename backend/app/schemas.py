from pydantic import BaseModel, Field, conint, confloat
from typing import List, Optional
from datetime import datetime

class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1)
    preco: confloat(ge=0)

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoOut(ProdutoBase):
    id: int

    class Config:
        from_attributes = True

class ItemPedido(BaseModel):
    produto_id: int
    nome: str = Field(..., min_length=1)
    quantidade: conint(gt=0)
    preco: confloat(ge=0)

class PedidoCreate(BaseModel):
    mesa: int
    garcom: str = Field(..., min_length=1)
    observacoes: Optional[str] = None
    itens: List[ItemPedido]

class ItemPedidoOut(ItemPedido):
    pass

class PedidoOut(BaseModel):
    id: int
    mesa: int
    garcom: str
    observacoes: Optional[str]
    timestamp: datetime
    itens: List[ItemPedidoOut]

    class Config:
        from_attributes = True
