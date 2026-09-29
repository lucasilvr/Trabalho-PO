from biblioteca.multas.domain import model
from biblioteca.multas.adapters.repository import SqlAlchemyMultaRepository
from biblioteca.multas.entrypoints.flask_app import app, get_session

def test_api_processa_pagamento_com_sucesso():
    session = get_session()
    SqlAlchemyMultaRepository(session).add(
        model.Multa(id_multa="M01", id_leitor="L01", dias_atraso=2, taxa_por_dia=5.0)
    )
    session.commit()

    response = app.test_client().post("/multas/M01/pagar", json={"valor": 10.0, "data": "2026-09-29"})

    assert response.status_code == 200
    assert response.json["message"] == "Pagamento efetuado!"

def test_api_retorna_400_para_multa_inexistente():
    response = app.test_client().post("/multas/M99/pagar", json={"valor": 10.0, "data": "2026-09-29"})

    assert response.status_code == 400
