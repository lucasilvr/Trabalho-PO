import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from biblioteca.emprestimo.adapters import orm
from biblioteca.emprestimo.entrypoints.flask_app import create_app


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


def test_api_retorna_404_para_atraso_de_item_inexistente(client):
    response = client.get(
        "/emprestimos/ITEM-999/atraso",
        query_string={
            "data_referencia": "2026-09-12",
        },
    )

    assert response.status_code == 404


def test_api_consulta_atraso_usa_tolerancia_da_categoria(client):
    response_emprestimo = client.post(
        "/emprestimos",
        json={
            "id_item": "ITEM-015",
            "id_exemplar": "EX-015",
            "data_emprestimo": "2026-09-01",
            "data_prevista_devolucao": "2026-09-10",
            "categoria_leitor": "Professor",
        },
    )

    assert response_emprestimo.status_code == 201
    assert response_emprestimo.get_json()["categoria_leitor"] == "Professor"

    dentro_da_tolerancia = client.get(
        "/emprestimos/ITEM-015/atraso",
        query_string={
            "data_referencia": "2026-09-13",
        },
    )

    assert dentro_da_tolerancia.status_code == 200
    assert dentro_da_tolerancia.get_json()["atrasado"] is False

    fora_da_tolerancia = client.get(
        "/emprestimos/ITEM-015/atraso",
        query_string={
            "data_referencia": "2026-09-14",
        },
    )

    assert fora_da_tolerancia.status_code == 200
    assert fora_da_tolerancia.get_json()["atrasado"] is True


def test_api_rejeita_categoria_de_leitor_invalida(client):
    response = client.post(
        "/emprestimos",
        json={
            "id_item": "ITEM-016",
            "id_exemplar": "EX-016",
            "data_emprestimo": "2026-09-01",
            "data_prevista_devolucao": "2026-09-10",
            "categoria_leitor": 1,
        },
    )

    assert response.status_code == 400