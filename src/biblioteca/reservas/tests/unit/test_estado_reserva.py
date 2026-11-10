from datetime import datetime, timedelta
import pytest
from biblioteca.reservas.domain.model import (
    Reserva,
    ReservaPendente,
    ReservaDisponivel,
    ReservaExpirada,
    TransicaoInvalida,
    ESTADOS_RESERVA,
)

def make_reserva():
    return Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))

def test_estado_pendente_disponibiliza_a_reserva():
    reserva = make_reserva()
    data_disponivel = datetime(2026, 9, 23, 10, 0)

    ReservaPendente().disponibilizar(reserva, data_disponivel)

    assert reserva.status == "Disponivel"
    assert reserva.data_disponibilizacao == data_disponivel

def test_estado_pendente_nao_pode_expirar():
    with pytest.raises(TransicaoInvalida, match="RES-01"):
        ReservaPendente().expirar(make_reserva())

def test_estado_disponivel_expira_apos_o_prazo():
    reserva = make_reserva()
    reserva.data_disponibilizacao = datetime(2026, 9, 23, 10, 0)

    assert ReservaDisponivel().esta_expirada(reserva, datetime(2026, 9, 25, 9, 0)) is False
    assert ReservaDisponivel().esta_expirada(reserva, datetime(2026, 9, 25, 11, 0)) is True

def test_estado_disponivel_expira_a_reserva():
    reserva = make_reserva()

    ReservaDisponivel().expirar(reserva)

    assert reserva.status == "Expirada"

def test_estado_expirado_nao_permite_nenhuma_transicao():
    reserva = make_reserva()

    with pytest.raises(TransicaoInvalida):
        ReservaExpirada().disponibilizar(reserva, datetime(2026, 9, 23, 10, 0))
    with pytest.raises(TransicaoInvalida):
        ReservaExpirada().expirar(reserva)
    assert ReservaExpirada().esta_expirada(reserva, datetime(2026, 12, 1, 10, 0)) is False

def test_cada_status_tem_um_estado_correspondente():
    assert set(ESTADOS_RESERVA) == {"Pendente", "Disponivel", "Expirada"}
    assert all(estado.nome == status for status, estado in ESTADOS_RESERVA.items())
