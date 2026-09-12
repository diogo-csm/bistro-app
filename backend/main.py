from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Bistro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

produtos = [
    {"id": 1, "nome": "Café", "preco": 3.5},
    {"id": 2, "nome": "Pão de queijo", "preco": 2.0},
    {"id": 3, "nome": "Suco", "preco": 4.0}
]

@app.get("/produtos")
def listar_produtos():
    return produtos
