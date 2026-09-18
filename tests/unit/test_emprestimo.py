from datetime import date

from src.biblioteca.domain.model import ItemEmprestado


def test_item_emprestado_esta_atrasado_quando_prazo_expirou():    
    item = ItemEmprestado(
        id_item="ITEM-001",
        id_exemplar="EX-001",
        data_emprestimo=date(2026, 9, 1),
        data_prevista_devolucao=date(2026, 9, 10),
    )
    
    resultado = item.esta_atrasado(date(2026, 9, 12))
    
    assert resultado is True