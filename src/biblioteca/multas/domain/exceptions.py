class MultaNaoEncontrada(Exception):
    def __init__(self, id_multa: str):
        self.id_multa = id_multa
        super().__init__(f"Multa {id_multa} não encontrada.")

class ValorPagamentoInvalido(Exception):
    def __init__(self, valor: float):
        self.valor = valor
        super().__init__(f"O valor do pagamento R$ {valor:.2f} é inválido.")