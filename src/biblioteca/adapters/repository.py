import abc
from src.biblioteca.domain import model

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, livro: model.Livro):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, isbn: str) -> model.Livro:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self):
        raise NotImplementedError

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, livro: model.Livro):
        self.session.add(livro)

    def get(self, isbn: str) -> model.Livro:
        return self.session.query(model.Livro).filter_by(isbn=isbn).first()

    def list(self):
        return self.session.query(model.Livro).all()

class FakeRepository(AbstractRepository):
    def __init__(self, livros):
        self._livros = set(livros)

    def add(self, livro: model.Livro):
        self._livros.add(livro)

    def get(self, isbn: str) -> model.Livro:
        return next((l for l in self._livros if l.isbn == isbn), None)

    def list(self):
        return list(self._livros)