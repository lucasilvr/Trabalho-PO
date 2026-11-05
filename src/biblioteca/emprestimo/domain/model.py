from datetime import date

from biblioteca.emprestimo.domain.politicas import PoliticaAtraso, politica_para


class ItemEmprestado:
    def __init__(
        self,
        id_item: str,
        id_exemplar: str,
        data_emprestimo: date,
        data_prevista_devolucao: date,
        categoria_leitor: str | None = None,
        politica_atraso: PoliticaAtraso | None = None,
    ):
        self.id_item = id_item
        self.id_exemplar = id_exemplar
        self.data_emprestimo = data_emprestimo
        self.data_prevista_devolucao = data_prevista_devolucao
        self.data_devolucao: date | None = None
        self.categoria_leitor = categoria_leitor
        self.politica_atraso = politica_atraso or politica_para(categoria_leitor)

    @property
    def politica_atraso(self) -> PoliticaAtraso:
        """Estratégia em uso.

        Objetos reconstruídos pelo SQLAlchemy não passam pelo `__init__`, mas
        carregam `categoria_leitor` do banco, então a política é reencontrada
        pela categoria.
        """
        return getattr(self, "_politica_atraso", None) or politica_para(
            getattr(self, "categoria_leitor", None)
        )

    @politica_atraso.setter
    def politica_atraso(self, politica: PoliticaAtraso) -> None:
        self._politica_atraso = politica

    def esta_atrasado(self, data_referencia: date) -> bool:
        if self.data_devolucao is not None:
            return False
        return self.politica_atraso.esta_atrasado(
            self.data_prevista_devolucao,
            data_referencia,
        )

    def registrar_devolucao(self, data_devolucao: date) -> None:
        self.data_devolucao = data_devolucao
