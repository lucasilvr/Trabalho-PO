from datetime import date

from biblioteca.emprestimo.adapters.repository import AbstractRepository
from biblioteca.emprestimo.domain.model import ItemEmprestado


def registrar_emprestimo(
    repo: AbstractRepository,
    id_item: str,
    id_exemplar: str,
    data_emprestimo: date,
    data_prevista_devolucao: date,
) -> ItemEmprestado:
    item = ItemEmprestado(
        id_item=id_item,
        id_exemplar=id_exemplar,
        data_emprestimo=data_emprestimo,
        data_prevista_devolucao=data_prevista_devolucao,
    )

    repo.add(item)

    return item


def registrar_devolucao(
    repo: AbstractRepository,
    id_item: str,
    data_devolucao: date,
) -> ItemEmprestado:
    item = repo.get(id_item)
    item.registrar_devolucao(data_devolucao)

    return item


def consultar_atraso(
    repo: AbstractRepository,
    id_item: str,
    data_referencia: date,
) -> bool:
    item = repo.get(id_item)

    return item.esta_atrasado(data_referencia)