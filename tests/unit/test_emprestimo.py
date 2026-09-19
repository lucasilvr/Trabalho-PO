from datetime import date

from src.biblioteca.domain.model import ItemEmprestado


def test_item_emprestado_esta_atrasado_quando_prazo_expirou():
    # Arrange
    item = ItemEmprestado(
        id_item="ITEM-001",
        id_exemplar="EX-001",
        data_emprestimo=date(2026, 9, 1),
        data_prevista_devolucao=date(2026, 9, 10),
    )

    # Act
    resultado = item.esta_atrasado(date(2026, 9, 12))

    # Assert
    assert resultado is True

def test_registrar_devolucao_atualiza_data_e_remove_atraso():
    # Arrange
    item = ItemEmprestado(
        id_item="ITEM-002",
        id_exemplar="EX-002",
        data_emprestimo=date(2026, 9, 1),
        data_prevista_devolucao=date(2026, 9, 10),
    )

    # Act
    item.registrar_devolucao(date(2026, 9, 15))

    # Assert
    assert item.data_devolucao == date(2026, 9, 15)
    assert item.esta_atrasado(date(2026, 9, 15)) is False