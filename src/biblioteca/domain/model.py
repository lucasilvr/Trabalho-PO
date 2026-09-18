from datetime import date


class ItemEmprestado:
    def __init__(
        self,
        id_item: str,
        id_exemplar: str,
        data_emprestimo: date,
        data_prevista_devolucao: date,
    ):
        self.id_item = id_item
        self.id_exemplar = id_exemplar
        self.data_emprestimo = data_emprestimo
        self.data_prevista_devolucao = data_prevista_devolucao
        self.data_devolucao = None

    def esta_atrasado(self, data_referencia: date) -> bool:
        return (
            self.data_devolucao is None
            and data_referencia > self.data_prevista_devolucao
        )