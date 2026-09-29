from sqlalchemy import MetaData, Table, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import registry, relationship
from biblioteca.domain import model

metadata = MetaData()
mapper_registry = registry()

multas = Table(
    'multas', metadata,
    Column('id_multa', String(255), primary_key=True),
    Column('id_leitor', String(255)),
    Column('dias_atraso', Integer),
    Column('taxa_por_dia', Float),
    Column('valor_total', Float),
    Column('status', String(50))
)

pagamentos = Table(
    'pagamentos', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('multa_id', String(255), ForeignKey('multas.id_multa')),
    Column('valor', Float),
    Column('data', Date)
)

def start_mappers():
    mapper_registry.map_imperatively(
        model.Multa, multas,
        properties={'pagamentos': relationship(model.Pagamento, backref='multa', collection_class=list)}
    )
    mapper_registry.map_imperatively(model.Pagamento, pagamentos)