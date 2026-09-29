from src.biblioteca.manutencao.domain import model
from src.biblioteca.manutencao.adapters.repository import AbstractRepository

class OrdemServicoService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def criar_ordem_servico(
        self,
        id_ordem: str,
        laudo: model.LaudoAvaliacao,
        exemplar_disponivel: bool
    ) -> model.OrdemServico:

        ordem_servico = model.OrdemServico(
            id_ordem=id_ordem,
            laudo=laudo,
            exemplar_disponivel=exemplar_disponivel
        )

        self.repository.add(ordem_servico)

        return ordem_servico

    def executar_ordem_servico(
        self,
        id_ordem: str
    ) -> model.OrdemServico:
        ordem_servico = self.repository.get(id_ordem)

        ordem_servico.iniciar_execucao()

        return ordem_servico

    def buscar_ordem_servico(
        self,
        id_ordem: str
    ) -> model.OrdemServico:

        return self.repository.get(id_ordem)

    def listar_ordens_servico(self) -> list[model.OrdemServico]:

        return self.repository.list()

    def concluir_ordem_servico(
        self,
        id_ordem: str,
    ) -> model.OrdemServico:

        ordem_servico = self.repository.get(id_ordem)

        if ordem_servico is None:
            raise ValueError("Ordem de serviço não encontrada.")

        ordem_servico.concluir()

        return ordem_servico

    def cancelar_ordem_servico(
        self,
        id_ordem: str,
    ) -> model.OrdemServico:

        ordem_servico = self.repository.get(id_ordem)

        if ordem_servico is None:
            raise ValueError("Ordem de serviço não encontrada.")

        ordem_servico.cancelar()

        return ordem_servico