from datetime import datetime, timedelta
from src.biblioteca.domain.model import Reserva, FilaEspera

def test_exemplar_devolvido_transfere_direito_se_expirado():
    fila = FilaEspera("LIVRO-1")
    reserva1 = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 20, 10, 0))
    reserva2 = Reserva("RES-02", "LEITOR-2", "LIVRO-1", datetime(2026, 9, 21, 10, 0))
    fila.adicionar_reserva(reserva1)
    fila.adicionar_reserva(reserva2)
    
    data_devolucao = datetime(2026, 9, 22, 10, 0)
    fila.exemplar_devolvido(data_devolucao)
    
    assert reserva1.status == "Disponivel"
    assert reserva2.status == "Pendente"
    
    # Simula passagem de 49 horas
    data_atual = data_devolucao + timedelta(hours=49)
    fila.atualizar_fila(data_atual)
    
    assert reserva1.status == "Expirada"
    assert reserva2.status == "Disponivel"