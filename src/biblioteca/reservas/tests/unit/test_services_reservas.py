from datetime import datetime, timedelta
import pytest
from biblioteca.reservas.adapters.repository import FakeFilaEsperaRepository
from biblioteca.reservas.domain.model import FilaEspera, Reserva
from biblioteca.reservas.service_layer import services

class FakeSession:
    committed = False

    def commit(self):
        self.committed = True

def make_fila_com_duas_reservas():
    fila = FilaEspera("LIVRO-1")
    reserva1 = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))
    reserva2 = Reserva("RES-02", "LEITOR-2", "LIVRO-1", datetime(2026, 9, 23, 10, 0))
    fila.adicionar_reserva(reserva1)
    fila.adicionar_reserva(reserva2)
    return fila, reserva1, reserva2

def test_reservar_livro_cria_fila_quando_nao_existe():
    repo = FakeFilaEsperaRepository([])
    session = FakeSession()

    reserva = services.reservar_livro(
        "RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0), repo, session
    )

    assert repo.get("LIVRO-1").reservas == [reserva]
    assert session.committed is True

def test_reservar_livro_entra_no_final_da_fila():
    fila, reserva1, reserva2 = make_fila_com_duas_reservas()
    repo = FakeFilaEsperaRepository([fila])

    reserva3 = services.reservar_livro(
        "RES-03", "LEITOR-3", "LIVRO-1", datetime(2026, 9, 24, 10, 0), repo, FakeSession()
    )

    assert fila.reservas == [reserva1, reserva2, reserva3]

def test_registrar_devolucao_disponibiliza_para_primeiro_da_fila():
    fila, reserva1, reserva2 = make_fila_com_duas_reservas()
    repo = FakeFilaEsperaRepository([fila])
    session = FakeSession()

    services.registrar_devolucao("LIVRO-1", datetime(2026, 9, 24, 10, 0), repo, session)

    assert reserva1.status == "Disponivel"
    assert reserva2.status == "Pendente"
    assert session.committed is True

def test_atualizar_fila_transfere_direito_apos_48_horas():
    fila, reserva1, reserva2 = make_fila_com_duas_reservas()
    repo = FakeFilaEsperaRepository([fila])
    data_devolucao = datetime(2026, 9, 24, 10, 0)
    services.registrar_devolucao("LIVRO-1", data_devolucao, repo, FakeSession())

    services.atualizar_fila("LIVRO-1", data_devolucao + timedelta(hours=49), repo, FakeSession())

    assert reserva1.status == "Expirada"
    assert reserva2.status == "Disponivel"

def test_registrar_devolucao_de_livro_sem_fila_lanca_erro():
    repo = FakeFilaEsperaRepository([])

    with pytest.raises(services.FilaNaoEncontrada, match="LIVRO-999"):
        services.registrar_devolucao("LIVRO-999", datetime(2026, 9, 24, 10, 0), repo, FakeSession())
