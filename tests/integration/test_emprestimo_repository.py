from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.biblioteca.adapters import orm
from src.biblioteca.adapters.repository import SqlAlchemyRepository
from src.biblioteca.domain.model import ItemEmprestado


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")

    orm.start_mappers()
    orm.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    yield session

    session.close()
    orm.clear_mappers()


def test_sqlalchemy_repository_adiciona_e_busca_item(session):
    repo = SqlAlchemyRepository(session)

    item = ItemEmprestado(
        id_item="ITEM-005",
        id_exemplar="EX-005",
        data_emprestimo=date(2026, 9, 3),
        data_prevista_devolucao=date(2026, 9, 12),
    )

    repo.add(item)
    session.commit()

    resultado = repo.get("ITEM-005")

    assert resultado.id_item == "ITEM-005"
    assert resultado.id_exemplar == "EX-005"
    assert resultado.data_emprestimo == date(2026, 9, 3)
    assert resultado.data_prevista_devolucao == date(2026, 9, 12)
    assert resultado.data_devolucao is None


def test_sqlalchemy_repository_lista_itens(session):
    repo = SqlAlchemyRepository(session)

    item1 = ItemEmprestado(
        id_item="ITEM-006",
        id_exemplar="EX-006",
        data_emprestimo=date(2026, 9, 4),
        data_prevista_devolucao=date(2026, 9, 13),
    )

    item2 = ItemEmprestado(
        id_item="ITEM-007",
        id_exemplar="EX-007",
        data_emprestimo=date(2026, 9, 5),
        data_prevista_devolucao=date(2026, 9, 14),
    )

    repo.add(item1)
    repo.add(item2)
    session.commit()

    itens = repo.list()

    assert len(itens) == 2
    assert {item.id_item for item in itens} == {
        "ITEM-006",
        "ITEM-007",
    }