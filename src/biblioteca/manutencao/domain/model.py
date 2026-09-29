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
        id_laudo: str,
        id_item: str,
        descricao_dano: str,
        reparavel: bool,
        data_avaliacao: date
    ):
        self.id_laudo = id_laudo
        self.id_item = id_item
        self.descricao_dano = descricao_dano
        self.reparavel = reparavel
        self.data_avaliacao = data_avaliacao

class OrdemServico:
    def __init__(
        self,
        id_ordem: str,
        laudo: LaudoAvaliacao,
        exemplar_disponivel: bool
    ):
        if not exemplar_disponivel:
            raise ValueError("Não é possível criar uma ordem de serviço sem um exemplar disponível.")

        if not laudo.reparavel:
            raise ValueError("Não é possível criar uma ordem de serviço para um dano não reparável.")
        
        self.id_ordem = id_ordem
        self.laudo = laudo
        self.status = OrdemServicoStatus.ABERTA

    def iniciar_execucao(self):
        if self.status != OrdemServicoStatus.ABERTA:
            raise ValueError("A ordem de serviço só pode ser iniciada se estiver aberta.")
        self.status = OrdemServicoStatus.EM_EXECUCAO

    def concluir(self):
        if self.status != OrdemServicoStatus.EM_EXECUCAO:
            raise ValueError("A ordem de serviço só pode ser concluída se estiver em execução.")
        self.status = OrdemServicoStatus.CONCLUIDA

    def cancelar(self):
        if self.status in [OrdemServicoStatus.CONCLUIDA, OrdemServicoStatus.CANCELADA]:
            raise ValueError("Não é possível cancelar uma ordem de serviço concluída ou já cancelada.")
        self.status = OrdemServicoStatus.CANCELADA
        