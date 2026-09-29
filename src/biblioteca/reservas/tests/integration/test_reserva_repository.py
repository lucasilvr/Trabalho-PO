from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from biblioteca.reservas.adapters import orm
from biblioteca.reservas.adapters.repository import SqlAlchemyFilaEsperaRepository
from biblioteca.reservas.domain import model


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    orm.start_mappers()
    orm.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()
    orm.clear_mappers()


def test_repository_recupera_fila_com_reservas_em_ordem(session):
    fila = model.FilaEspera("LIVRO-1")
    fila.adicionar_reserva(model.Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0)))
    fila.adicionar_reserva(model.Reserva("RES-02", "LEITOR-2", "LIVRO-1", datetime(2026, 9, 23, 10, 0)))
    repo = SqlAlchemyFilaEsperaRepository(session)
    repo.add(fila)
    session.commit()
    session.expunge_all()

    recuperada = repo.get("LIVRO-1")

    assert recuperada is not fila
    assert [r.id_reserva for r in recuperada.reservas] == ["RES-01", "RES-02"]
    assert all(r.status == "Pendente" for r in recuperada.reservas)


def test_repository_persiste_mudanca_de_status(session):
    fila = model.FilaEspera("LIVRO-1")
    fila.adicionar_reserva(model.Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0)))
    repo = SqlAlchemyFilaEsperaRepository(session)
    repo.add(fila)
    session.commit()

    repo.get("LIVRO-1").exemplar_devolvido(datetime(2026, 9, 24, 10, 0))
    session.commit()
    session.expunge_all()

    reserva = repo.get("LIVRO-1").reservas[0]
    assert reserva.status == "Disponivel"
    assert reserva.data_disponibilizacao == datetime(2026, 9, 24, 10, 0)


def test_repository_retorna_none_para_fila_inexistente(session):
    repo = SqlAlchemyFilaEsperaRepository(session)

    assert repo.get("LIVRO-999") is None
    assert repo.list() == []
