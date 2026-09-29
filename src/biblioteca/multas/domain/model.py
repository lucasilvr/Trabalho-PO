from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class Pagamento:
    valor: float
    data: date

class Multa:
    def __init__(self, id_multa: str, id_leitor: str, dias_atraso: int, taxa_por_dia: float):
        self.id_multa = id_multa
        self.id_leitor = id_leitor
        self.dias_atraso = dias_atraso
        self.taxa_por_dia = taxa_por_dia
        self.valor_total = dias_atraso * taxa_por_dia
        self.status = "Pendente"
        self.pagamentos: List[Pagamento] = []

    def registrar_pagamento(self, pagamento: Pagamento):
        self.pagamentos.append(pagamento)
        total_pago = sum(p.valor for p in self.pagamentos)
        if total_pago >= self.valor_total:
            self.status = "Quitada"