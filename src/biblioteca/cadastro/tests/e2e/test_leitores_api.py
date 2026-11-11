import pytest
from biblioteca.cadastro.entrypoints.flask_app import app
from biblioteca.cadastro.adapters import orm

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_mappers():
    orm.clear_mappers()
    orm.start_mappers()
    yield
    orm.clear_mappers()

def test_cadastrar_leitor_retorna_201_com_id(client):
    dados = {
        "nome": "Isabella Motta",
        "email": "isa@api.com",
        "tipo_categoria": "Aluno"
    }
    
    resposta = client.post("/leitores", json=dados)
    
    assert resposta.status_code == 201
    assert "id_leitor" in resposta.json