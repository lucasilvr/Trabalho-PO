from datetime import datetime

from biblioteca.reservas.adapters.repository import AbstractFilaEsperaRepository
from biblioteca.reservas.domain.model import FilaEspera, Reserva


class FilaNaoEncontrada(Exception):
    pass


def _obter_fila(repo: AbstractFilaEsperaRepository, id_livro: str) -> FilaEspera:
    fila = repo.get(id_livro)
    if fila is None:
        raise FilaNaoEncontrada(f"Fila de espera do livro {id_livro} não encontrada")
    return fila


def reservar_livro(
    repo: AbstractFilaEsperaRepository,
    id_reserva: str,
    id_leitor: str,
    id_livro: str,
    data_reserva: datetime,
) -> Reserva:
    fila = repo.get(id_livro)
    if fila is None:
        fila = FilaEspera(id_livro)
        repo.add(fila)

    reserva = Reserva(id_reserva, id_leitor, id_livro, data_reserva)
    fila.adicionar_reserva(reserva)

    return reserva


def registrar_devolucao_exemplar(
    repo: AbstractFilaEsperaRepository,
    id_livro: str,
    data_hora: datetime,
) -> FilaEspera:
    fila = _obter_fila(repo, id_livro)
    fila.exemplar_devolvido(data_hora)

    return fila


def atualizar_fila(
    repo: AbstractFilaEsperaRepository,
    id_livro: str,
    data_hora_atual: datetime,
) -> FilaEspera:
    fila = _obter_fila(repo, id_livro)
    fila.atualizar_fila(data_hora_atual)

    return fila


def consultar_fila(
    repo: AbstractFilaEsperaRepository,
    id_livro: str,
) -> FilaEspera:
    return _obter_fila(repo, id_livro)
