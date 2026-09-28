from datetime import date

from src.biblioteca.adapters.repository import FakeRepository
from src.biblioteca.domain.model import ItemEmprestado
from src.biblioteca.service_layer import services


def test_registrar_emprestimo_adiciona_item_ao_repositorio():
    repo = FakeRepository([])

    item = services.registrar_emprestimo(
        repo=repo,
        id_item="ITEM-008",
        id_exemplar="EX-008",
        data_emprestimo=date(2026, 9, 28),
        data_prevista_devolucao=date(2026, 10, 5),
    )

    resultado = repo.get("ITEM-008")

    assert resultado is item
    assert resultado.id_exemplar == "EX-008"
    assert resultado.data_emprestimo == date(2026, 9, 28)
    assert resultado.data_prevista_devolucao == date(2026, 10, 5)
    assert resultado.data_devolucao is None


def test_registrar_devolucao_atualiza_item():
    item = ItemEmprestado(
        id_item="ITEM-009",
        id_exemplar="EX-009",
        data_emprestimo=date(2026, 9, 20),
        data_prevista_devolucao=date(2026, 9, 30),
    )

    repo = FakeRepository([item])

    resultado = services.registrar_devolucao(
        repo=repo,
        id_item="ITEM-009",
        data_devolucao=date(2026, 9, 28),
    )

    assert resultado is item
    assert resultado.data_devolucao == date(2026, 9, 28)
    assert resultado.esta_atrasado(date(2026, 9, 28)) is False


def test_consultar_atraso_retorna_true_quando_item_esta_atrasado():
    item = ItemEmprestado(
        id_item="ITEM-010",
        id_exemplar="EX-010",
        data_emprestimo=date(2026, 9, 1),
        data_prevista_devolucao=date(2026, 9, 10),
    )

    repo = FakeRepository([item])

    resultado = services.consultar_atraso(
        repo=repo,
        id_item="ITEM-010",
        data_referencia=date(2026, 9, 12),
    )

    assert resultado is True


def test_consultar_atraso_retorna_false_quando_item_nao_esta_atrasado():
    item = ItemEmprestado(
        id_item="ITEM-011",
        id_exemplar="EX-011",
        data_emprestimo=date(2026, 9, 1),
        data_prevista_devolucao=date(2026, 9, 10),
    )

    repo = FakeRepository([item])

    resultado = services.consultar_atraso(
        repo=repo,
        id_item="ITEM-011",
        data_referencia=date(2026, 9, 10),
    )

    assert resultado is False