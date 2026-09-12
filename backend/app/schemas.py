from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    categoria: Optional[str] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoOut(ProdutoBase):
    id: int
    class Config:
        orm_mode = True

class ItemPedido(BaseModel):
    produto_id: Optional[int] = None
    nome: str
    quantidade: int
    preco: float

class PedidoCreate(BaseModel):
    mesa: Optional[str] = None
    garcom: Optional[str] = None
    observacoes: Optional[str] = None
    itens: List[ItemPedido]

class PedidoOut(BaseModel):
    id: int
    mesa: Optional[str]
    garcom: Optional[str]
    observacoes: Optional[str]
    timestamp: datetime
    itens: List[ItemPedido]
    class Config:
        orm_mode = True
