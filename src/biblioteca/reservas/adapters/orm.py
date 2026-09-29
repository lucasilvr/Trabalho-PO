from sqlalchemy import Column, DateTime, String, Table, ForeignKey
from sqlalchemy.orm import registry, relationship
from biblioteca.reservas.domain import model

mapper_registry = registry()
metadata = mapper_registry.metadata

reservas = Table(
    "reservas",
    metadata,
    Column("id_reserva", String(50), primary_key=True),
    Column("id_leitor", String(50), nullable=False),
    Column("id_livro", String(50), ForeignKey("filas_espera.id_livro"), nullable=False),
    Column("data_reserva", DateTime, nullable=False),
    Column("status", String(20), nullable=False),
    Column("data_disponibilizacao", DateTime, nullable=True),
)

filas_espera = Table(
    "filas_espera",
    metadata,
    Column("id_livro", String(50), primary_key=True),
)

def start_mappers():
    mapper_registry.map_imperatively(
        model.Reserva,
        reservas,
    )

    mapper_registry.map_imperatively(
        model.FilaEspera,
        filas_espera,
        properties={
            "reservas": relationship(
                model.Reserva,
                collection_class=list,
            )
        }
    )

def clear_mappers():
    mapper_registry.dispose()