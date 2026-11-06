from datetime import datetime, timedelta

PRAZO_RETIRADA_PADRAO_HORAS = 48

class TransicaoInvalida(Exception):
    pass

class EstadoReserva:
    nome = ""

    def disponibilizar(self, reserva, data_hora: datetime) -> None:
        raise TransicaoInvalida(f"Reserva {reserva.id_reserva} com status {self.nome} nao pode ser disponibilizada")

    def expirar(self, reserva) -> None:
        raise TransicaoInvalida(f"Reserva {reserva.id_reserva} com status {self.nome} nao pode expirar")

    def esta_expirada(self, reserva, data_hora_atual: datetime) -> bool:
        return False

class ReservaPendente(EstadoReserva):
    nome = "Pendente"

    def disponibilizar(self, reserva, data_hora: datetime) -> None:
        reserva.status = ReservaDisponivel.nome
        reserva.data_disponibilizacao = data_hora

class ReservaDisponivel(EstadoReserva):
    nome = "Disponivel"

    def esta_expirada(self, reserva, data_hora_atual: datetime) -> bool:
        return (data_hora_atual - reserva.data_disponibilizacao) > timedelta(hours=reserva.prazo_retirada_horas)

    def expirar(self, reserva) -> None:
        reserva.status = ReservaExpirada.nome

class ReservaExpirada(EstadoReserva):
    nome = "Expirada"

ESTADOS_RESERVA = {
    ReservaPendente.nome: ReservaPendente(),
    ReservaDisponivel.nome: ReservaDisponivel(),
    ReservaExpirada.nome: ReservaExpirada(),
}

class Reserva:
    def __init__(
        self,
        id_reserva: str,
        id_leitor: str,
        id_livro: str,
        data_reserva: datetime,
        prazo_retirada_horas: int = PRAZO_RETIRADA_PADRAO_HORAS
    ):
        self.id_reserva = id_reserva
        self.id_leitor = id_leitor
        self.id_livro = id_livro
        self.data_reserva = data_reserva
        self.status = "Pendente"
        self.data_disponibilizacao: datetime | None = None
        self.prazo_retirada_horas = prazo_retirada_horas

    def disponibilizar(self, data_hora: datetime) -> None:
        self.status = "Disponivel"
        self.data_disponibilizacao = data_hora

    def esta_expirada(self, data_hora_atual: datetime) -> bool:
        if self.status == "Disponivel" and self.data_disponibilizacao is not None:
            return (data_hora_atual - self.data_disponibilizacao) > timedelta(hours=self.prazo_retirada_horas)
        return False

    def expirar(self) -> None:
        self.status = "Expirada"

    def __eq__(self, other):
        if not isinstance(other, Reserva):
            return False
        return other.id_reserva == self.id_reserva

    def __hash__(self):
        return hash(self.id_reserva)
        
class FilaEspera:
    def __init__(self, id_livro: str):
        self.id_livro = id_livro
        self.reservas: list[Reserva] = []

    def __eq__(self, other):
        if not isinstance(other, FilaEspera):
            return False
        return other.id_livro == self.id_livro

    def __hash__(self):
        return hash(self.id_livro)

    def adicionar_reserva(self, reserva: Reserva) -> None:
        self.reservas.append(reserva)

    def exemplar_devolvido(self, data_hora: datetime) -> None:
        pendentes = [r for r in self.reservas if r.status == "Pendente"]
        if pendentes:
            pendentes[0].disponibilizar(data_hora)

    def atualizar_fila(self, data_hora_atual: datetime) -> None:
        for reserva in self.reservas:
            if reserva.esta_expirada(data_hora_atual):
                reserva.expirar()
                self.exemplar_devolvido(data_hora_atual)