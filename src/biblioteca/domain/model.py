from datetime import datetime, timedelta

class Reserva:
    def __init__(
        self,
        id_reserva: str,
        id_leitor: str,
        id_livro: str,
        data_reserva: datetime
    ):
        self.id_reserva = id_reserva
        self.id_leitor = id_leitor
        self.id_livro = id_livro
        self.data_reserva = data_reserva
        self.status = "Pendente"
        self.data_disponibilizacao: datetime | None = None

    def disponibilizar(self, data_hora: datetime) -> None:
        self.status = "Disponivel"
        self.data_disponibilizacao = data_hora

    def esta_expirada(self, data_hora_atual: datetime) -> bool:
        if self.status == "Disponivel" and self.data_disponibilizacao is not None:
            return (data_hora_atual - self.data_disponibilizacao) > timedelta(hours=48)
        return False

    def expirar(self) -> None:
        self.status = "Expirada"