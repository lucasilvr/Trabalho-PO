from datetime import datetime, timedelta

import pytest

from biblioteca.reservas.adapters.repository import FakeFilaEsperaRepository
from biblioteca.reservas.domain.model import FilaEspera, Reserva
from biblioteca.reservas.service_layer import services


def test_reservar_livro_cria_fila_quando_nao_existe():
    repo = FakeFilaEsperaRepository([])

    reserva = services.reservar_livro(
        repo=repo,
        id_reserva="RES-01",
        id_leitor="LEITOR-1",
        id_livro="LIVRO-1",
        data_reserva=datetime(2026, 9, 22, 10, 0),
    )

    fila = repo.get("LIVRO-1")
    assert fila is not None
    assert fila.reservas == [reserva]
    assert reserva.status == "Pendente"


def test_reservar_livro_entra_no_final_da_fila_existente():
    fila = FilaEspera("LIVRO-1")
    primeira = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))
    fila.adicionar_reserva(primeira)
    repo = FakeFilaEsperaRepository([fila])

    segunda = services.reservar_livro(
        repo=repo,
        id_reserva="RES-02",
        id_leitor="LEITOR-2",
        id_livro="LIVRO-1",
        data_reserva=datetime(2026, 9, 23, 10, 0),
    )

    assert fila.reservas == [primeira, segunda]


def test_registrar_devolucao_disponibiliza_para_primeiro_da_fila():
    fila = FilaEspera("LIVRO-1")
    primeira = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))
    segunda = Reserva("RES-02", "LEITOR-2", "LIVRO-1", datetime(2026, 9, 23, 10, 0))
    fila.adicionar_reserva(primeira)
    fila.adicionar_reserva(segunda)
    repo = FakeFilaEsperaRepository([fila])

    services.registrar_devolucao_exemplar(
        repo=repo,
        id_livro="LIVRO-1",
        data_hora=datetime(2026, 9, 24, 10, 0),
    )

    assert primeira.status == "Disponivel"
    assert segunda.status == "Pendente"


def test_atualizar_fila_transfere_direito_apos_48_horas():
    fila = FilaEspera("LIVRO-1")
    primeira = Reserva("RES-01", "LEITOR-1", "LIVRO-1", datetime(2026, 9, 22, 10, 0))
    segunda = Reserva("RES-02", "LEITOR-2", "LIVRO-1", datetime(2026, 9, 23, 10, 0))
    fila.adicionar_reserva(primeira)
    fila.adicionar_reserva(segunda)
    repo = FakeFilaEsperaRepository([fila])
    data_devolucao = datetime(2026, 9, 24, 10, 0)
    services.registrar_devolucao_exemplar(repo, "LIVRO-1", data_devolucao)

    services.atualizar_fila(
        repo=repo,
        id_livro="LIVRO-1",
        data_hora_atual=data_devolucao + timedelta(hours=49),
    )

    assert primeira.status == "Expirada"
    assert segunda.status == "Disponivel"


def test_consultar_fila_inexistente_lanca_erro():
    repo = FakeFilaEsperaRepository([])

    with pytest.raises(services.FilaNaoEncontrada):
        services.consultar_fila(repo=repo, id_livro="LIVRO-999")
