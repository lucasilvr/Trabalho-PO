import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from biblioteca.reservas.adapters import orm
from biblioteca.reservas.entrypoints.flask_app import create_app


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


def reservar(client, id_reserva, id_leitor, data_reserva, id_livro="LIVRO-1"):
    return client.post(
        "/reservas",
        json={
            "id_reserva": id_reserva,
            "id_leitor": id_leitor,
            "id_livro": id_livro,
            "data_reserva": data_reserva,
        },
    )


def test_api_cria_reserva(client):
    response = reservar(client, "RES-01", "LEITOR-1", "2026-09-22T10:00:00")

    assert response.status_code == 201

    dados = response.get_json()

    assert dados["id_reserva"] == "RES-01"
    assert dados["id_livro"] == "LIVRO-1"
    assert dados["status"] == "Pendente"
    assert dados["data_disponibilizacao"] is None


def test_api_rejeita_reserva_sem_campos_obrigatorios(client):
    response = client.post("/reservas", json={"id_reserva": "RES-01"})

    assert response.status_code == 400


def test_api_devolucao_disponibiliza_para_primeiro_da_fila(client):
    reservar(client, "RES-01", "LEITOR-1", "2026-09-22T10:00:00")
    reservar(client, "RES-02", "LEITOR-2", "2026-09-23T10:00:00")

    response = client.post(
        "/filas/LIVRO-1/devolucao",
        json={"data_hora": "2026-09-24T10:00:00"},
    )

    assert response.status_code == 200

    reservas = response.get_json()["reservas"]

    assert [r["status"] for r in reservas] == ["Disponivel", "Pendente"]
    assert reservas[0]["data_disponibilizacao"] == "2026-09-24T10:00:00"


def test_api_atualizacao_transfere_direito_apos_48_horas(client):
    reservar(client, "RES-01", "LEITOR-1", "2026-09-22T10:00:00")
    reservar(client, "RES-02", "LEITOR-2", "2026-09-23T10:00:00")
    client.post("/filas/LIVRO-1/devolucao", json={"data_hora": "2026-09-24T10:00:00"})

    response = client.post(
        "/filas/LIVRO-1/atualizacao",
        json={"data_hora_atual": "2026-09-26T11:00:00"},
    )

    assert response.status_code == 200

    reservas = response.get_json()["reservas"]

    assert [r["status"] for r in reservas] == ["Expirada", "Disponivel"]


def test_api_consulta_fila(client):
    reservar(client, "RES-01", "LEITOR-1", "2026-09-22T10:00:00")

    response = client.get("/filas/LIVRO-1")

    assert response.status_code == 200
    assert response.get_json()["id_livro"] == "LIVRO-1"
    assert len(response.get_json()["reservas"]) == 1


def test_api_retorna_404_para_fila_inexistente(client):
    response = client.post(
        "/filas/LIVRO-999/devolucao",
        json={"data_hora": "2026-09-24T10:00:00"},
    )

    assert response.status_code == 404
