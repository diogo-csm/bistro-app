from sqlalchemy.orm import Session
from . import models, schemas

def get_produtos(db: Session):
    return db.query(models.Produto).all()

def create_produto(db: Session, produto: schemas.ProdutoCreate):
    db_prod = models.Produto(nome=produto.nome, preco=produto.preco, categoria=produto.categoria)
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

def create_pedido(db: Session, pedido: schemas.PedidoCreate):
    db_pedido = models.Pedido(mesa=pedido.mesa, garcom=pedido.garcom, observacoes=pedido.observacoes)
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    for it in pedido.itens:
        db_item = models.PedidoItem(
            pedido_id=db_pedido.id,
            produto_id=it.produto_id,
            nome=it.nome,
            quantidade=it.quantidade,
            preco=it.preco
        )
        db.add(db_item)
    db.commit()
    return db_pedido

def get_pedidos(db: Session):
    return db.query(models.Pedido).all()

def get_pedido_itens(db: Session, pedido_id: int):
    return db.query(models.PedidoItem).filter(models.PedidoItem.pedido_id == pedido_id).all()
