import pytest
from biblioteca.entrypoints.flask_app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_cadastrar_leitor_retorna_201_com_id(client):
    dados = {
        "nome": "Isabella Motta",
        "email": "isa@api.com",
        "tipo_categoria": "Aluno"
    }
    
    resposta = client.post("/leitores", json=dados)
    
    assert resposta.status_code == 201
    assert "id_leitor" in resposta.json