from datetime import date

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.biblioteca.domain import model
from src.biblioteca.adapters import orm
from src.biblioteca.adapters.repository import SqlAlchemyRepository

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")

    orm.map_ordem_servico()
    orm.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    yield session

    session.close()
    orm.clear_mappings()

def test_salvar_e_buscar_ordem_servico(session):
    repo = SqlAlchemyRepository(session)

    # Arrange
    laudo = model.LaudoAvaliacao(
        id_laudo="LAUDO-001",
        id_item="ITEM-001",
        descricao_dano="Capa danificada",
        reparavel=True,
        data_avaliacao=date.today()
    )

    ordem_servico = model.OrdemServico(
        id_ordem="OS-001",  
        laudo=laudo,
        exemplar_disponivel=True
    )

    # Act
    repo.add(ordem_servico)
    session.commit()

    ordem_busca = repo.get("OS-001")

    # Assert
    assert ordem_busca.id_ordem == ordem_servico.id_ordem
    assert ordem_busca.laudo.id_laudo == ordem_servico.laudo.id_laudo

def test_listar_ordens_servico(session):
    repo = SqlAlchemyRepository(session)

    # Arrange
    laudo1 = model.LaudoAvaliacao(
        id_laudo="LAUDO-001",
        id_item="ITEM-001",
        descricao_dano="Capa danificada",
        reparavel=True,
        data_avaliacao=date.today()
    )

    ordem1 = model.OrdemServico(
        id_ordem="OS-001",  
        laudo=laudo1,
        exemplar_disponivel=True
    )

    laudo2 = model.LaudoAvaliacao(
        id_laudo="LAUDO-002",
        id_item="ITEM-002",
        descricao_dano="Páginas rasgadas",
        reparavel=True,
        data_avaliacao=date.today()
    )

    ordem2 = model.OrdemServico(
        id_ordem="OS-002",  
        laudo=laudo2,
        exemplar_disponivel=True
    )

    # Act
    repo.add(ordem1)
    repo.add(ordem2)
    session.commit()

    ordens_listadas = repo.list()

    # Assert
    assert len(ordens_listadas) == 2
    assert {ordem.id_ordem for ordem in ordens_listadas} == {"OS-001", "OS-002"}