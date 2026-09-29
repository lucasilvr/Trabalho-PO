from datetime import datetime
from biblioteca.reservas.adapters.repository import AbstractFilaEsperaRepository
from biblioteca.reservas.domain.model import FilaEspera, Reserva

class FilaNaoEncontrada(Exception):
    pass

def reservar_livro(
    id_reserva: str,
    id_leitor: str,
    id_livro: str,
    data_reserva: datetime,
    repo: AbstractFilaEsperaRepository,
    session,
) -> Reserva:
    fila = repo.get(id_livro)
    if fila is None:
        fila = FilaEspera(id_livro)
        repo.add(fila)
    reserva = Reserva(id_reserva, id_leitor, id_livro, data_reserva)
    fila.adicionar_reserva(reserva)
    session.commit()
    return reserva

def registrar_devolucao(
    id_livro: str,
    data_hora: datetime,
    repo: AbstractFilaEsperaRepository,
    session,
) -> FilaEspera:
    fila = repo.get(id_livro)
    if fila is None:
        raise FilaNaoEncontrada(f"Fila de espera do livro {id_livro} nao encontrada")
    fila.exemplar_devolvido(data_hora)
    session.commit()
    return fila

def atualizar_fila(
    id_livro: str,
    data_hora_atual: datetime,
    repo: AbstractFilaEsperaRepository,
    session,
) -> FilaEspera:
    fila = repo.get(id_livro)
    if fila is None:
        raise FilaNaoEncontrada(f"Fila de espera do livro {id_livro} nao encontrada")
    fila.atualizar_fila(data_hora_atual)
    session.commit()
    return fila
