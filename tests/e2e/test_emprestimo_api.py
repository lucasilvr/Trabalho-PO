import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.biblioteca.adapters import orm
from src.biblioteca.entrypoints.flask_app import create_app


@pytest.fixture
def client():
    engine = create_engine("sqlite:///:memory:")

    orm.start_mappers()
    orm.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    app = create_app(session)
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

    session.close()
    orm.clear_mappers()


def test_api_registra_emprestimo(client):
    response = client.post(
        "/emprestimos",
        json={
            "id_item": "ITEM-012",
            "id_exemplar": "EX-012",
            "data_emprestimo": "2026-09-28",
            "data_prevista_devolucao": "2026-10-05",
        },
    )

    assert response.status_code == 201

    dados = response.get_json()

    assert dados["id_item"] == "ITEM-012"
    assert dados["id_exemplar"] == "EX-012"
    assert dados["data_emprestimo"] == "2026-09-28"
    assert dados["data_prevista_devolucao"] == "2026-10-05"
    assert dados["data_devolucao"] is None


def test_api_registra_devolucao(client):
    response_emprestimo = client.post(
        "/emprestimos",
        json={
            "id_item": "ITEM-013",
            "id_exemplar": "EX-013",
            "data_emprestimo": "2026-09-20",
            "data_prevista_devolucao": "2026-09-30",
        },
    )

    assert response_emprestimo.status_code == 201

    response = client.post(
        "/emprestimos/ITEM-013/devolucao",
        json={
            "data_devolucao": "2026-09-28",
        },
    )

    assert response.status_code == 200

    dados = response.get_json()

    assert dados["id_item"] == "ITEM-013"
    assert dados["data_devolucao"] == "2026-09-28"


def test_api_consulta_atraso(client):
    response_emprestimo = client.post(
        "/emprestimos",
        json={
            "id_item": "ITEM-014",
            "id_exemplar": "EX-014",
            "data_emprestimo": "2026-09-01",
            "data_prevista_devolucao": "2026-09-10",
        },
    )

    assert response_emprestimo.status_code == 201

    response = client.get(
        "/emprestimos/ITEM-014/atraso",
        query_string={
            "data_referencia": "2026-09-12",
        },
    )

    assert response.status_code == 200

    dados = response.get_json()

    assert dados["id_item"] == "ITEM-014"
    assert dados["atrasado"] is True


def test_api_retorna_404_para_item_inexistente(client):
    response = client.post(
        "/emprestimos/ITEM-999/devolucao",
        json={
            "data_devolucao": "2026-09-28",
        },
    )

    assert response.status_code == 404