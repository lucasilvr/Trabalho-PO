from datetime import datetime
import pytest
from sqlalchemy import create_engine, text
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

def test_repository_can_retrieve_a_fila_with_reservas(session):
    session.execute(text("INSERT INTO filas_espera (id_livro) VALUES ('LIVRO-1')"))
    session.execute(text(
        "INSERT INTO reservas (id_reserva, id_leitor, id_livro, data_reserva, status) VALUES "
        "('RES-02', 'LEITOR-2', 'LIVRO-1', '2026-09-23 10:00:00.000000', 'Pendente'),"
        "('RES-01', 'LEITOR-1', 'LIVRO-1', '2026-09-22 10:00:00.000000', 'Pendente')"
    ))

    repo = SqlAlchemyFilaEsperaRepository(session)
    retrieved = repo.get("LIVRO-1")

    assert retrieved == model.FilaEspera("LIVRO-1")
    assert [r.id_reserva for r in retrieved.reservas] == ["RES-01", "RES-02"]

def test_repository_can_list_filas(session):
    session.execute(text("INSERT INTO filas_espera (id_livro) VALUES ('LIVRO-1'), ('LIVRO-2')"))

    repo = SqlAlchemyFilaEsperaRepository(session)

    assert set(repo.list()) == {model.FilaEspera("LIVRO-1"), model.FilaEspera("LIVRO-2")}

def test_repository_persiste_prazo_de_retirada_da_reserva(session):
    fila = model.FilaEspera("LIVRO-1")
    fila.adicionar_reserva(model.Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0), prazo_retirada_horas=72))
    repo = SqlAlchemyFilaEsperaRepository(session)
    repo.add(fila)
    session.commit()

    rows = session.execute(text("SELECT id_reserva, prazo_retirada_horas FROM reservas"))
    assert list(rows) == [("RES-01", 72)]

def test_reserva_inserida_sem_prazo_usa_o_padrao_de_48_horas(session):
    session.execute(text("INSERT INTO filas_espera (id_livro) VALUES ('LIVRO-1')"))
    session.execute(text(
        "INSERT INTO reservas (id_reserva, id_leitor, id_livro, data_reserva, status) VALUES "
        "('RES-01', 'LEITOR-1', 'LIVRO-1', '2026-09-22 10:00:00.000000', 'Pendente')"
    ))

    repo = SqlAlchemyFilaEsperaRepository(session)

    assert repo.get("LIVRO-1").reservas[0].prazo_retirada_horas == 48

def test_reserva_carregada_do_banco_volta_ao_estado_correto(session):
    session.execute(text("INSERT INTO filas_espera (id_livro) VALUES ('LIVRO-1')"))
    session.execute(text(
        "INSERT INTO reservas (id_reserva, id_leitor, id_livro, data_reserva, status, data_disponibilizacao) VALUES "
        "('RES-01', 'LEITOR-1', 'LIVRO-1', '2026-09-22 10:00:00.000000', 'Disponivel', '2026-09-23 10:00:00.000000'),"
        "('RES-02', 'LEITOR-2', 'LIVRO-1', '2026-09-23 10:00:00.000000', 'Expirada', NULL)"
    ))

    repo = SqlAlchemyFilaEsperaRepository(session)
    disponivel, expirada = repo.get("LIVRO-1").reservas

    assert isinstance(disponivel.estado, model.ReservaDisponivel)
    assert isinstance(expirada.estado, model.ReservaExpirada)
    with pytest.raises(model.TransicaoInvalida):
        disponivel.disponibilizar(datetime(2026, 9, 24, 10, 0))
    with pytest.raises(model.TransicaoInvalida):
        expirada.disponibilizar(datetime(2026, 9, 24, 10, 0))

def test_transicao_de_estado_e_persistida_no_banco(session):
    fila = model.FilaEspera("LIVRO-1")
    fila.adicionar_reserva(model.Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0)))
    repo = SqlAlchemyFilaEsperaRepository(session)
    repo.add(fila)
    session.commit()

    repo.get("LIVRO-1").exemplar_devolvido(datetime(2026, 9, 23, 10, 0))
    session.commit()
    repo.get("LIVRO-1").atualizar_fila(datetime(2026, 9, 25, 11, 0))
    session.commit()

    rows = session.execute(text("SELECT id_reserva, status FROM reservas"))
    assert list(rows) == [("RES-01", "Expirada")]
