from datetime import date
from biblioteca.multas.domain import model
from biblioteca.multas.adapters.repository import AbstractMultaRepository

def pagar_multa(id_multa: str, valor: float, data_pgto: date, repo: AbstractMultaRepository, session):
    multa = repo.get(id_multa)
    if multa is None:
        raise ValueError(f"Multa {id_multa} não encontrada.")
    
    multa.registrar_pagamento(model.Pagamento(valor=valor, data=data_pgto))
    session.commit()