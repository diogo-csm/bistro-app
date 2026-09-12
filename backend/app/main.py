from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bistro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/produtos", response_model=list[schemas.ProdutoOut])
def listar_produtos(db: Session = Depends(get_db)):
    return crud.get_produtos(db)

@app.post("/produtos", response_model=schemas.ProdutoOut)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return crud.create_produto(db, produto)

@app.post("/pedido")
def criar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    db_pedido = crud.create_pedido(db, pedido)
    return {"status": "ok", "pedido_id": db_pedido.id, "timestamp": db_pedido.timestamp.isoformat()}

@app.get("/pedidos", response_model=list[schemas.PedidoOut])
def listar_pedidos(db: Session = Depends(get_db)):
    pedidos = crud.get_pedidos(db)
    result = []
    for p in pedidos:
        itens = crud.get_pedido_itens(db, p.id)
        itens_out = [{"produto_id": it.produto_id, "nome": it.nome, "quantidade": it.quantidade, "preco": it.preco} for it in itens]
        result.append({
            "id": p.id,
            "mesa": p.mesa,
            "garcom": p.garcom,
            "observacoes": p.observacoes,
            "timestamp": p.timestamp,
            "itens": itens_out
        })
    return result
