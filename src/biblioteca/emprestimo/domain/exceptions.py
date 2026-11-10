class ItemNaoEncontrado(Exception):
    """Erro de domínio para item de empréstimo inexistente.

    Faz parte do contrato do repositório: qualquer implementação deve
    levantar esta exceção quando o item solicitado não existir.
    """

    def __init__(self, id_item: str):
        self.id_item = id_item
        super().__init__(f"Item de empréstimo {id_item} não encontrado.")
