from enum import Enum
from datetime import date

class OrdemServicoStatus(Enum):
    ABERTA = "aberta"
    EM_EXECUCAO = "em_execucao"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"

class LaudoAvaliacao:
    def __init__(
        self,
        id_item: str,
        descricao_dano: str,
        reparavel: bool,
        data_avaliacao: date
    ):
        self.id_item = id_item
        self.descricao_dano = descricao_dano
        self.reparavel = reparavel
        self.data_avaliacao = data_avaliacao

class OrdemServico:
    def __init__(
        self,
        id_ordem: str,
        laudo: LaudoAvaliacao
    ):
        self.id_ordem = id_ordem
        self.laudo = laudo
        self.status = OrdemServicoStatus.ABERTA
        