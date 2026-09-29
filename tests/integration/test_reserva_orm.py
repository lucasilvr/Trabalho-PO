from datetime import datetime
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.biblioteca.adapters import orm
from src.biblioteca.adapters.repository import SqlAlchemyFilaEsperaRepository
from src.biblioteca.domain import model

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    orm.start_mappers()
    orm.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()
    orm.clear_mappers()

def test_repository_can_save_a_fila_espera(session):
    fila = model.FilaEspera("LIVRO-XYZ")
    reserva = model.Reserva("RES-10", "LEITOR-2", "LIVRO-XYZ", datetime(2026, 9, 24, 10, 0))
    fila.adicionar_reserva(reserva)
    
    repo = SqlAlchemyFilaEsperaRepository(session)
    repo.add(fila)
    session.commit()
    
    rows = list(session.execute(text('SELECT id_livro FROM filas_espera')))
    assert rows == [("LIVRO-XYZ",)]