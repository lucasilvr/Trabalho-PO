from abc import ABC, abstractmethod
from datetime import date, timedelta


class PoliticaAtraso(ABC):
    """Strategy para a regra de atraso de um empréstimo.

    Permite variar a tolerância sem alterar ItemEmprestado. Novas
    políticas podem ser adicionadas apenas criando outra subclasse.
    """

    @abstractmethod
    def esta_atrasado(
        self,
        data_prevista_devolucao: date,
        data_referencia: date,
    ) -> bool:
        raise NotImplementedError


class SemTolerancia(PoliticaAtraso):
    """Comportamento histórico: atrasa no primeiro dia após o prazo."""

    def esta_atrasado(
        self,
        data_prevista_devolucao: date,
        data_referencia: date,
    ) -> bool:
        return data_referencia > data_prevista_devolucao


class ToleranciaEmDias(PoliticaAtraso):
    """Concede uma quantidade fixa de dias de tolerância após o prazo."""

    def __init__(self, dias: int):
        if dias < 0:
            raise ValueError("A tolerância não pode ser negativa.")
        self.dias = dias

    def esta_atrasado(
        self,
        data_prevista_devolucao: date,
        data_referencia: date,
    ) -> bool:
        prazo_com_tolerancia = data_prevista_devolucao + timedelta(days=self.dias)
        return data_referencia > prazo_com_tolerancia


POLITICAS_POR_CATEGORIA: dict[str, PoliticaAtraso] = {
    "Aluno": ToleranciaEmDias(1),
    "Professor": ToleranciaEmDias(3),
}


def politica_para(categoria_leitor: str | None) -> PoliticaAtraso:
    """Seleciona a estratégia de atraso a partir da categoria do leitor.

    Categorias desconhecidas ou ausentes usam `SemTolerancia`, preservando
    o comportamento da Fase 1.
    """
    return POLITICAS_POR_CATEGORIA.get(categoria_leitor, SemTolerancia())
