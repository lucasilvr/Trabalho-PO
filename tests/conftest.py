from datetime import date
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.biblioteca.domain import model
from src.biblioteca.adapters import orm

@pytest.fixture
def laudo_reparavel():
    return model.LaudoAvaliacao(
        id_laudo="LAUDO-001",
        id_item="ITEM-001",
        descricao_dano="Capa danificada",
        reparavel=True,
        data_avaliacao=date.today()
    )

@pytest.fixture
def laudo_irreparavel():
    return model.LaudoAvaliacao(
        id_laudo="LAUDO-002",
        id_item="ITEM-002",
        descricao_dano="Páginas rasgadas",
        reparavel=False,
        data_avaliacao=date.today()
    )

@pytest.fixture
def ordem_servico(laudo_reparavel):
    def criar(id_ordem: str):
        return model.OrdemServico(
            id_ordem=id_ordem,  
            laudo=laudo_reparavel,
            exemplar_disponivel=True
        )

    return criar

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")

    orm.map_ordem_servico()
    orm.metadata.create_all(engine)

    session = sessionmaker(bind=engine)()

    yield session

    session.close()
    orm.clear_mappings()