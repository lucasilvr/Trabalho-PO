from sqlalchemy import Table, MetaData, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import registry, composite  # <-- composite importado aqui
from biblioteca.cadastro.domain import model

mapper_registry = registry()
metadata = mapper_registry.metadata

leitores_table = Table(
    "leitores",
    metadata,
    Column("id_leitor", String(255), primary_key=True),
    Column("nome", String(255), nullable=False),
    Column("email", String(255), nullable=False),
    Column("categoria_nome", String(50), nullable=False),
    Column("limite_emprestimos", Integer, nullable=False),
    Column("emprestimos_ativos", Integer, nullable=False, default=0),
    Column("ativo", Boolean, nullable=False, default=True),
    Column("data_cadastro", Date, nullable=False),
)

def start_mappers():
    mapper_registry.map_imperatively(
        model.Leitor,
        leitores_table,
        properties={
            "categoria": composite(
                model.CategoriaLeitor, 
                leitores_table.c.categoria_nome, 
                leitores_table.c.limite_emprestimos
            )
        }
    )