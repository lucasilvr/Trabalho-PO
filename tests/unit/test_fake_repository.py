from datetime import date

from src.biblioteca.adapters.repository import FakeRepository
from src.biblioteca.domain.model import ItemEmprestado


def test_fake_repository_adiciona_busca_e_lista_itens():
    item1 = ItemEmprestado(
        id_item="ITEM-003",
        id_exemplar="EX-003",
        data_emprestimo=date(2026, 9, 1),
        data_prevista_devolucao=date(2026, 9, 10),
    )

    item2 = ItemEmprestado(
        id_item="ITEM-004",
        id_exemplar="EX-004",
        data_emprestimo=date(2026, 9, 2),
        data_prevista_devolucao=date(2026, 9, 11),
    )

    repo = FakeRepository([])

    repo.add(item1)
    repo.add(item2)

    resultado = repo.get("ITEM-003")
    itens = repo.list()

    assert resultado is item1
    assert len(itens) == 2
    assert {item.id_item for item in itens} == {
        "ITEM-003",
        "ITEM-004",
    }