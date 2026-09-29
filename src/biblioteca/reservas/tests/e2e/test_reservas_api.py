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
    yield app.test_client()
    session.close()
    orm.clear_mappers()

def test_happy_path_transfere_reserva_apos_48_horas(client):
    r = client.post("/reservas", json={"id_reserva": "RES-01", "id_leitor": "LEITOR-1", "id_livro": "LIVRO-1", "data_reserva": "2026-09-22T10:00:00"})
    assert r.status_code == 201
    client.post("/reservas", json={"id_reserva": "RES-02", "id_leitor": "LEITOR-2", "id_livro": "LIVRO-1", "data_reserva": "2026-09-23T10:00:00"})

    r = client.post("/filas/LIVRO-1/devolucao", json={"data_hora": "2026-09-24T10:00:00"})
    assert r.status_code == 200

    r = client.post("/filas/LIVRO-1/atualizacao", json={"data_hora_atual": "2026-09-26T11:00:00"})
    assert r.status_code == 200
    assert [res["status"] for res in r.json["reservas"]] == ["Expirada", "Disponivel"]

def test_unhappy_path_retorna_404_para_livro_sem_fila(client):
    r = client.post("/filas/LIVRO-999/devolucao", json={"data_hora": "2026-09-24T10:00:00"})
    assert r.status_code == 404
    assert "LIVRO-999" in r.json["message"]
