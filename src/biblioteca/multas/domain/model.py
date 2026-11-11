from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import List
from biblioteca.multas.domain.exceptions import ValorPagamentoInvalido

class CalculoMulta(ABC):
    """Component: Interface base para cálculo do valor da multa."""
    @abstractmethod
    def calcular(self, dias_atraso: int, taxa_por_dia: float) -> float:
        pass

class CalculoMultaBase(CalculoMulta):
    """ConcreteComponent: Cálculo básico e linear da multa (dias * taxa)."""
    def calcular(self, dias_atraso: int, taxa_por_dia: float) -> float:
        return dias_atraso * taxa_por_dia

class DecoradorMulta(CalculoMulta):
    """Decorator: Classe abstrata decoradora que mantém referência a um objeto CalculoMulta."""
    def __init__(self, calculo: CalculoMulta):
        self._calculo = calculo

    def calcular(self, dias_atraso: int, taxa_por_dia: float) -> float:
        return self._calculo.calcular(dias_atraso, taxa_por_dia)

class DecoradorJurosMora(DecoradorMulta):
    """ConcreteDecorator: Adiciona 10% de juros de mora para atrasos superiores a 5 dias."""
    def calcular(self, dias_atraso: int, taxa_por_dia: float) -> float:
        valor_base = self._calculo.calcular(dias_atraso, taxa_por_dia)
        if dias_atraso > 5:
            return valor_base * 1.10
        return valor_base

class DecoradorTaxaAdministrativa(DecoradorMulta):
    """ConcreteDecorator: Adiciona taxa administrativa fixa de R$ 5,00 ao cálculo."""
    def calcular(self, dias_atraso: int, taxa_por_dia: float) -> float:
        return self._calculo.calcular(dias_atraso, taxa_por_dia) + 5.0

@dataclass
class Pagamento:
    valor: float
    data: date

    def __post_init__(self):
        if self.valor <= 0:
            raise ValorPagamentoInvalido(self.valor)

class Multa:
    def __init__(
        self, 
        id_multa: str, 
        id_leitor: str, 
        dias_atraso: int, 
        taxa_por_dia: float,
        calculo: CalculoMulta = None
    ):
        self.id_multa = id_multa
        self.id_leitor = id_leitor
        self.dias_atraso = dias_atraso
        self.taxa_por_dia = taxa_por_dia
        self.calculo = calculo or CalculoMultaBase()
        self.valor_total = self.calculo.calcular(dias_atraso, taxa_por_dia)
        self.status = "Pendente"
        self.pagamentos: List[Pagamento] = []

    def registrar_pagamento(self, pagamento: Pagamento):
        self.pagamentos.append(pagamento)
        total_pago = sum(p.valor for p in self.pagamentos)
        if total_pago >= self.valor_total:
            self.status = "Quitada"