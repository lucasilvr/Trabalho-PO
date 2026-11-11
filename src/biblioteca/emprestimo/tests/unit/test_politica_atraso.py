from datetime import date

import pytest

from biblioteca.emprestimo.domain.model import ItemEmprestado
from biblioteca.emprestimo.domain.politicas import ToleranciaEmDias


def criar_item(politica=None) -> ItemEmprestado:
    return ItemEmprestado(
        id_item="ITEM-020",
        id_exemplar="EX-020",
        data_emprestimo=date(2026, 9, 1),
        data_prevista_devolucao=date(2026, 9, 10),
        politica_atraso=politica,
    )


def test_sem_politica_mantem_comportamento_original():
    item = criar_item()

    assert item.esta_atrasado(date(2026, 9, 10)) is False
    assert item.esta_atrasado(date(2026, 9, 11)) is True


def test_tolerancia_de_um_dia_para_aluno():
    item = criar_item(ToleranciaEmDias(1))

    assert item.esta_atrasado(date(2026, 9, 11)) is False
    assert item.esta_atrasado(date(2026, 9, 12)) is True


def test_tolerancia_de_tres_dias_para_professor():
    item = criar_item(ToleranciaEmDias(3))

    assert item.esta_atrasado(date(2026, 9, 13)) is False
    assert item.esta_atrasado(date(2026, 9, 14)) is True


def test_politica_pode_ser_trocada_sem_alterar_a_entidade():
    item = criar_item()

    assert item.esta_atrasado(date(2026, 9, 11)) is True

    item.politica_atraso = ToleranciaEmDias(2)

    assert item.esta_atrasado(date(2026, 9, 11)) is False


def test_item_devolvido_nao_fica_atrasado_mesmo_com_tolerancia():
    item = criar_item(ToleranciaEmDias(3))
    item.registrar_devolucao(date(2026, 9, 20))

    assert item.esta_atrasado(date(2026, 9, 30)) is False


def test_tolerancia_negativa_e_rejeitada():
    with pytest.raises(ValueError):
        ToleranciaEmDias(-1)
