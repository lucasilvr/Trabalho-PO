from datetime import datetime, timedelta
import pytest
from biblioteca.reservas.domain.model import (
    Reserva,
    ReservaPendente,
    ReservaDisponivel,
    ReservaExpirada,
    TransicaoInvalida,
)

def test_reserva_nova_comeca_como_pendente():
    reserva = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))
    assert reserva.status == "Pendente"

def test_reserva_expira_apos_48_horas_disponivel():
    reserva = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))
    data_disponivel = datetime(2026, 9, 23, 10, 0)
    reserva.disponibilizar(data_disponivel)
    
    data_consulta = data_disponivel + timedelta(hours=49)
    assert reserva.esta_expirada(data_consulta) is True
    

def test_reservas_com_mesmo_id_sao_iguais():
    reserva1 = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))
    reserva2 = Reserva("RES-01", "LEITOR-2", "LIVRO-2", datetime(2026, 9, 23, 10, 0))
    assert reserva1 == reserva2

def test_reserva_sem_prazo_informado_usa_prazo_padrao_de_48_horas():
    reserva = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))
    assert reserva.prazo_retirada_horas == 48

def test_reserva_com_prazo_de_72_horas_nao_expira_apos_49_horas():
    reserva = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0), prazo_retirada_horas=72)
    data_disponivel = datetime(2026, 9, 23, 10, 0)
    reserva.disponibilizar(data_disponivel)

    assert reserva.esta_expirada(data_disponivel + timedelta(hours=49)) is False
    assert reserva.esta_expirada(data_disponivel + timedelta(hours=73)) is True

def test_reserva_expirada_nao_pode_ser_disponibilizada_novamente():
    reserva = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))
    reserva.disponibilizar(datetime(2026, 9, 23, 10, 0))
    reserva.expirar()

    with pytest.raises(TransicaoInvalida):
        reserva.disponibilizar(datetime(2026, 9, 26, 10, 0))
    assert reserva.status == "Expirada"

def test_reserva_disponivel_nao_reinicia_o_prazo_ao_ser_disponibilizada_de_novo():
    reserva = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))
    data_disponivel = datetime(2026, 9, 23, 10, 0)
    reserva.disponibilizar(data_disponivel)

    with pytest.raises(TransicaoInvalida):
        reserva.disponibilizar(datetime(2026, 9, 24, 10, 0))
    assert reserva.data_disponibilizacao == data_disponivel

def test_reserva_pendente_nao_pode_expirar():
    reserva = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))

    with pytest.raises(TransicaoInvalida):
        reserva.expirar()
    assert reserva.status == "Pendente"

def test_reserva_delega_o_comportamento_ao_estado_atual():
    reserva = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))
    assert isinstance(reserva.estado, ReservaPendente)

    reserva.disponibilizar(datetime(2026, 9, 23, 10, 0))
    assert isinstance(reserva.estado, ReservaDisponivel)

    reserva.expirar()
    assert isinstance(reserva.estado, ReservaExpirada)
