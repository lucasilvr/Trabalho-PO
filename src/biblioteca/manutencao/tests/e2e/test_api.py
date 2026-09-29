import pytest

from src.biblioteca.manutencao.entrypoints.flask_app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def test_criar_ordem_servico(client):

    response = client.post(
        "/ordens-servico",
        json={
            "id_ordem": "OS-001",
            "id_laudo": "LAUDO-001",
            "id_item": "ITEM-001",
            "descricao_dano": "Capa rasgada",
            "reparavel": True,
            "data_avaliacao": "2026-09-29",
            "exemplar_disponivel": True
        }
    )

    assert response.status_code == 201

    body = response.get_json()

    assert body["id_ordem"] == "OS-001"
    assert body["status"] == "aberta"

def test_buscar_ordem_servico(client):

    client.post(
        "/ordens-servico",
        json={
            "id_ordem": "OS-002",
            "id_laudo": "LAUDO-002",
            "id_item": "ITEM-002",
            "descricao_dano": "Páginas rasgadas",
            "reparavel": True,
            "data_avaliacao": "2026-09-29",
            "exemplar_disponivel": True
        }
    )

    response = client.get(
        "/ordens-servico/OS-002"
    )

    assert response.status_code == 200

    body = response.get_json()

    assert body["id_ordem"] == "OS-002"

def test_iniciar_ordem_servico(client):

    client.post(
        "/ordens-servico",
        json={
            "id_ordem": "OS-003",
            "id_laudo": "LAUDO-003",
            "id_item": "ITEM-003",
            "descricao_dano": "Capa rasgada",
            "reparavel": True,
            "data_avaliacao": "2026-09-29",
            "exemplar_disponivel": True
        }
    )

    response = client.post(
        "/ordens-servico/OS-003/iniciar"
    )

    assert response.status_code == 200

    body = response.get_json()

    assert body["status"] == "em_execucao"

def test_concluir_ordem_servico(client):

    client.post(
        "/ordens-servico",
        json={
            "id_ordem": "OS-004",
            "id_laudo": "LAUDO-004",
            "id_item": "ITEM-004",
            "descricao_dano": "Capa rasgada",
            "reparavel": True,
            "data_avaliacao": "2026-09-29",
            "exemplar_disponivel": True
        }
    )

    client.post(
        "/ordens-servico/OS-004/iniciar"
    )

    response = client.post(
        "/ordens-servico/OS-004/concluir"
    )

    assert response.status_code == 200

    body = response.get_json()

    assert body["status"] == "concluida"

def test_cancelar_ordem_servico(client):

    client.post(
        "/ordens-servico",
        json={
            "id_ordem": "OS-005",
            "id_laudo": "LAUDO-005",
            "id_item": "ITEM-005",
            "descricao_dano": "Capa rasgada",
            "reparavel": True,
            "data_avaliacao": "2026-09-29",
            "exemplar_disponivel": True
        }
    )

    response = client.post(
        "/ordens-servico/OS-005/cancelar"
    )

    assert response.status_code == 200

    body = response.get_json()

    assert body["status"] == "cancelada"