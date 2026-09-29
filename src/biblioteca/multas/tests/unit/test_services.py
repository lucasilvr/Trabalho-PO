from datetime import date
from biblioteca.multas.domain import model
from biblioteca.multas.adapters import repository
from biblioteca.multas.service_layer import services

def test_pagar_multa_atualiza_status(session): 
    multa = model.Multa(id_multa="M01", id_leitor="L99", dias_atraso=2, taxa_por_dia=5.0)
    repo = repository.FakeMultaRepository([multa])
    
    services.pagar_multa("M01", 10.0, date.today(), repo, session)
    
    assert repo.get("M01").status == "Quitada"