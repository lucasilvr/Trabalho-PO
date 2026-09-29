from abc import ABC, abstractmethod

from src.biblioteca.domain import model

class AbstractRepository(ABC):
    @abstractmethod
    def add(self, ordem_servico: model.OrdemServico) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, id_ordem: str) -> model.OrdemServico:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[model.OrdemServico]:
        raise NotImplementedError

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, ordem_servico: model.OrdemServico) -> None:
        self.session.add(ordem_servico)

    def get(self, id_ordem: str) -> model.OrdemServico:
        return (
            self.session.query(model.OrdemServico)
            .filter_by(id_ordem=id_ordem)
            .one()
        )

    def list(self) -> list[model.OrdemServico]:
        return self.session.query(model.OrdemServico).all()

class FakeRepository(AbstractRepository):
    def __init__(self, ordens_servico):
        self._ordens_servico = set(ordens_servico)

    def add(self, ordem_servico: model.OrdemServico) -> None:
        self._ordens_servico.add(ordem_servico)

    def get(self, id_ordem: str) -> model.OrdemServico:
        return next(
            (ordem for ordem in self._ordens_servico if ordem.id_ordem == id_ordem),
            None
        )

    def list(self) -> list[model.OrdemServico]:
        return list(self._ordens_servico)
