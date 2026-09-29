import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, clear_mappers
from biblioteca.acervo.adapters import orm
from biblioteca.acervo.domain import model
from biblioteca.acervo.adapters import repository

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    orm.metadata.create_all(engine)
    orm.start_mappers()
    yield sessionmaker(bind=engine)()
    clear_mappers()

def test_repository_can_save_a_livro(session):
    livro = model.Livro(isbn="12345", titulo="O Hobbit", autor="Tolkien")
    exemplar = model.Exemplar(id_exemplar="EX-001", status="disponivel")
    livro.adicionar_exemplar(exemplar)
    repo = repository.SqlAlchemyRepository(session)
    repo.add(livro)
    session.commit()
    rows = session.execute(text('SELECT isbn, titulo, autor, ativo FROM "livros"'))
    assert list(rows) == [("12345", "O Hobbit", "Tolkien", 1)]
