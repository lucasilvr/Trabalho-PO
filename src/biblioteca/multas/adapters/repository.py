import abc
from biblioteca.multas.domain import model

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
        return next((m for m in self._multas if m.id_multa == id_multa), None)

class SqlAlchemyMultaRepository(AbstractMultaRepository):
    def __init__(self, session):
        self.session = session

    def add(self, multa: model.Multa):
        self.session.add(multa)

    def get(self, id_multa: str) -> model.Multa:
        return self.session.query(model.Multa).filter_by(id_multa=id_multa).first()