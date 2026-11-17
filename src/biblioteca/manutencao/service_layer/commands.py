from abc import ABC, abstractmethod
from src.biblioteca.manutencao.domain.model import OrdemServico

class Command(ABC):
    @abstractmethod
    def execute(self) -> OrdemServico:
        pass


class ConcluirOrdemServicoCommand(Command):
    def __init__(self, ordem_servico: OrdemServico):
        self.ordem_servico = ordem_servico

    def execute(self) -> OrdemServico:
        self.ordem_servico.concluir()
        return self.ordem_servico