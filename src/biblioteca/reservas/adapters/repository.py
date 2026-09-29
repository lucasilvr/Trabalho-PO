import abc
from biblioteca.reservas.domain import model

class AbstractFilaEsperaRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, fila: model.FilaEspera):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id_livro: str) -> model.FilaEspera:
        raise NotImplementedError

class SqlAlchemyFilaEsperaRepository(AbstractFilaEsperaRepository):
    def __init__(self, session):
        self.session = session

    def add(self, fila: model.FilaEspera):
        self.session.add(fila)

    def get(self, id_livro: str) -> model.FilaEspera:
        return self.session.query(model.FilaEspera).filter_by(id_livro=id_livro).first()