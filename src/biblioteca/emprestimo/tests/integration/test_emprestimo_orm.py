from datetime import date

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from biblioteca.emprestimo.adapters import orm
from biblioteca.emprestimo.domain import model


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")

    orm.start_mappers()
    orm.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    yield session

    session.close()
    orm.clear_mappers()


def test_item_emprestado_pode_ser_carregado_pelo_orm(session):
    session.execute(
        text(
            """
            INSERT INTO itens_emprestados (
                id_item,
                id_exemplar,
                data_emprestimo,
                data_prevista_devolucao,
                data_devolucao
            )
            VALUES (
                'ITEM-001',
                'EX-001',
                '2026-09-01',
                '2026-09-10',
                NULL
            )
            """
        )
    )
    session.commit()

    item = (
        session.query(model.ItemEmprestado)
        .filter_by(id_item="ITEM-001")
        .one()
    )

    assert item.id_item == "ITEM-001"
    assert item.id_exemplar == "EX-001"
    assert item.data_emprestimo == date(2026, 9, 1)
    assert item.data_prevista_devolucao == date(2026, 9, 10)
    assert item.data_devolucao is None


def test_item_recarregado_do_banco_usa_politica_da_categoria(session):
    session.execute(
        text(
            """
            INSERT INTO itens_emprestados (
                id_item,
                id_exemplar,
                data_emprestimo,
                data_prevista_devolucao,
                data_devolucao,
                categoria_leitor
            )
            VALUES (
                'ITEM-002',
                'EX-002',
                '2026-09-01',
                '2026-09-10',
                NULL,
                'Professor'
            )
            """
        )
    )
    session.commit()

    session.expunge_all()

    item = (
        session.query(model.ItemEmprestado)
        .filter_by(id_item="ITEM-002")
        .one()
    )

    assert item.categoria_leitor == "Professor"
    assert item.esta_atrasado(date(2026, 9, 13)) is False
    assert item.esta_atrasado(date(2026, 9, 14)) is True