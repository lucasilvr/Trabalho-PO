from sqlalchemy import Column, Date, String, Table
from sqlalchemy.orm import registry

from src.biblioteca.domain import model


mapper_registry = registry()
metadata = mapper_registry.metadata


itens_emprestados = Table(
    "itens_emprestados",
    metadata,
    Column("id_item", String(50), primary_key=True),
    Column("id_exemplar", String(50), nullable=False),
    Column("data_emprestimo", Date, nullable=False),
    Column("data_prevista_devolucao", Date, nullable=False),
    Column("data_devolucao", Date, nullable=True),
)


def start_mappers():
    mapper_registry.map_imperatively(
        model.ItemEmprestado,
        itens_emprestados,
    )


def clear_mappers():
    mapper_registry.dispose()