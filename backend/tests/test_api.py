from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_produto_and_list():
    r = client.post("/produtos", json={"nome": "TesteUnit", "preco": 2.5})
    assert r.status_code == 200
    data = r.json()
    assert data["nome"] == "TesteUnit"
    assert data["preco"] == 2.5

def test_create_pedido_with_existing_produto():
    r = client.post("/produtos", json={"nome": "ProdutoParaPedido", "preco": 3.0})
    produto = r.json()
    pedido_payload = {
        "mesa": 1,
        "garcom": "Ana",
        "observacoes": "sem cebola",
        "itens": [
            {"produto_id": produto["id"], "nome": produto["nome"], "quantidade": 2, "preco": produto["preco"]}
        ]
    }
    r2 = client.post("/pedido", json=pedido_payload)
    assert r2.status_code == 200
    assert "pedido_id" in r2.json()

def test_create_pedido_with_missing_produto():
    pedido_payload = {
        "mesa": 2,
        "garcom": "Carlos",
        "observacoes": None,
        "itens": [
            {"produto_id": 999999, "nome": "Inexistente", "quantidade": 1, "preco": 1.0}
        ]
    }
    r = client.post("/pedido", json=pedido_payload)
    assert r.status_code == 404

def test_list_pedidos_returns_structure():
    r = client.get("/pedidos")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        p = data[0]
        assert "id" in p and "itens" in p
