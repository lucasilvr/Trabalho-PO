from sqlalchemy import Table, MetaData, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import registry, relationship
from src.biblioteca.domain import model

mapper_registry = registry()
metadata = mapper_registry.metadata

livros = Table(
    "livros",
    metadata,
    Column("isbn", String(255), primary_key=True),
    Column("titulo", String(255), nullable=False),
    Column("autor", String(255), nullable=False),
    Column("ativo", Boolean, default=True),
)

exemplares = Table(
    "exemplares",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("id_exemplar", String(255), nullable=False),
    Column("status", String(50), nullable=False),
    Column("livro_isbn", ForeignKey("livros.isbn")),
)

def start_mappers():
    linhas_mapper = mapper_registry.map_imperatively(model.Exemplar, exemplares)
    mapper_registry.map_imperatively(
        model.Livro,
        livros,
        properties={
            "exemplares": relationship(
                linhas_mapper,
                collection_class=list,
            )
        },
    )