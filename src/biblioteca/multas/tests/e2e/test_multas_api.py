import pytest
from datetime import date
from sqlalchemy.orm import clear_mappers
from biblioteca.multas.adapters import orm, repository
from biblioteca.multas.domain import model
from biblioteca.multas.entrypoints.flask_app import app, get_session

@pytest.fixture(autouse=True)
def setup_mappers_e_banco():
    clear_mappers()
    orm.start_mappers()
    yield
    clear_mappers()

def test_api_processa_pagamento_com_sucesso():
    session = get_session()
    repo = repository.SqlAlchemyMultaRepository(session)
    repo.add(
        model.Multa(id_multa="M01", id_leitor="L01", dias_atraso=2, taxa_por_dia=5.0)
    )
    session.commit()

    response = app.test_client().post("/multas/M01/pagar", json={"valor": 10.0, "data": "2026-09-29"})

    assert response.status_code == 200
    assert response.json["message"] == "Pagamento efetuado!"
    
def test_api_retorna_404_para_multa_inexistente():
    response = app.test_client().post("/multas/M99/pagar", json={"valor": 10.0, "data": "2026-09-29"})
    assert response.status_code == 404