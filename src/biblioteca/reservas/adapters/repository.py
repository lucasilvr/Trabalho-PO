import abc
from biblioteca.reservas.domain import model

class AbstractFilaEsperaRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, fila: model.FilaEspera):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id_livro: str) -> model.FilaEspera | None:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> list[model.FilaEspera]:
        raise NotImplementedError

class SqlAlchemyFilaEsperaRepository(AbstractFilaEsperaRepository):
    def __init__(self, session):
        self.session = session

    def add(self, fila: model.FilaEspera):
        self.session.add(fila)

    def get(self, id_livro: str) -> model.FilaEspera | None:
        return self.session.query(model.FilaEspera).filter_by(id_livro=id_livro).first()

    def list(self) -> list[model.FilaEspera]:
        return self.session.query(model.FilaEspera).all()

class FakeFilaEsperaRepository(AbstractFilaEsperaRepository):
    def __init__(self, filas):
        self._filas = set(filas)

    def add(self, fila: model.FilaEspera):
        self._filas.add(fila)

    def get(self, id_livro: str) -> model.FilaEspera | None:
        return next((f for f in self._filas if f.id_livro == id_livro), None)

    def list(self) -> list[model.FilaEspera]:
        return list(self._filas)
