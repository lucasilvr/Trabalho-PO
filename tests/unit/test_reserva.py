from datetime import datetime, timedelta
from src.biblioteca.domain.model import Reserva

def test_reserva_nova_comeca_como_pendente():
    reserva = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))
    assert reserva.status == "Pendente"

def test_reserva_expira_apos_48_horas_disponivel():
    reserva = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))
    data_disponivel = datetime(2026, 9, 23, 10, 0)
    reserva.disponibilizar(data_disponivel)
    
    data_consulta = data_disponivel + timedelta(hours=49)
    assert reserva.esta_expirada(data_consulta) is True
    
