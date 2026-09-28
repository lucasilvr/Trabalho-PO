import abc
from biblioteca.domain import model

class AbstractLeitorRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, leitor: model.Leitor):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id_leitor: str) -> model.Leitor:
        raise NotImplementedError

class FakeLeitorRepository(AbstractLeitorRepository):
    def __init__(self, leitores=None):
        self._leitores = set(leitores or [])

    def add(self, leitor: model.Leitor):
        self._leitores.add(leitor)

    def get(self, id_leitor: str) -> model.Leitor:
        return next((l for l in self._leitores if l.id_leitor == id_leitor), None)