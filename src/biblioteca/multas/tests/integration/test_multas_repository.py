from biblioteca.multas.domain import model
from biblioteca.multas.adapters.repository import SqlAlchemyMultaRepository

def test_repository_pode_salvar_e_buscar_multa(session):
    multa = model.Multa(id_multa="M99", id_leitor="L01", dias_atraso=3, taxa_por_dia=2.0)
    repo = SqlAlchemyMultaRepository(session)
    
    repo.add(multa)
    session.commit()
    
    recuperada = repo.get("M99")
    assert recuperada is not None
    assert recuperada.id_multa == "M99"
    assert recuperada.status == "Pendente"