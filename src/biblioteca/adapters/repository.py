import abc
from biblioteca.domain import model

class AbstractMultaRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, multa: model.Multa):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id_multa: str) -> model.Multa:
        raise NotImplementedError

class FakeMultaRepository(AbstractMultaRepository):
    def __init__(self, multas):
        self._multas = set(multas)

    def add(self, multa: model.Multa):
        self._multas.add(multa)

    def get(self, id_multa: str):
        return next((m for m in self._multas if m.id_leitor == id_multa), None)