from sqlalchemy import Table, Column, String, Date, Boolean, ForeignKey, Enum
from sqlalchemy.orm import registry, relationship

from src.biblioteca.manutencao.domain import model

mapper_registry = registry()
metadata = mapper_registry.metadata

laudo_avaliacao = Table(
    "laudo_avaliacao",
    metadata,
    Column("id_laudo", String(50), primary_key=True),
    Column("id_item", String(50), nullable=False),
    Column("descricao_dano", String(255), nullable=False),
    Column("reparavel", Boolean, nullable=False),
    Column("data_avaliacao", Date, nullable=False)
)

ordens_servico = Table(
    "ordens_servico",
    metadata,
    Column("id_ordem", String(50), primary_key=True),
    Column(
        "id_laudo", 
        String(50), 
        ForeignKey("laudo_avaliacao.id_laudo"),
        nullable=False
    ),
    Column("status", Enum(model.OrdemServicoStatus), nullable=False)
)

def map_ordem_servico():    
    laudo_mapper = mapper_registry.map_imperatively(
        model.LaudoAvaliacao,
        laudo_avaliacao
    )

    mapper_registry.map_imperatively(
        model.OrdemServico,
        ordens_servico,
        properties={
            "laudo": relationship(
                laudo_mapper,
                uselist=False
            )
        }
    )

def clear_mappings():
    mapper_registry.dispose()