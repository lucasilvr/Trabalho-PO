from abc import ABC, abstractmethod

from sqlalchemy.orm.exc import NoResultFound

from biblioteca.emprestimo.domain import model
from biblioteca.emprestimo.domain.exceptions import ItemNaoEncontrado


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, item: model.ItemEmprestado) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, id_item: str) -> model.ItemEmprestado:
        """Retorna o item ou levanta ItemNaoEncontrado.

        O contrato é o mesmo para todas as implementações, permitindo
        substituir o repositório real pelo fake sem alterar os chamadores.
        """
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[model.ItemEmprestado]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, item: model.ItemEmprestado) -> None:
        self.session.add(item)

    def get(self, id_item: str) -> model.ItemEmprestado:
        try:
            return (
                self.session.query(model.ItemEmprestado)
                .filter_by(id_item=id_item)
                .one()
            )
        except NoResultFound as exc:
            raise ItemNaoEncontrado(id_item) from exc

    def list(self) -> list[model.ItemEmprestado]:
        return self.session.query(model.ItemEmprestado).all()


class FakeRepository(AbstractRepository):
    def __init__(self, items):
        self._items = set(items)

    def add(self, item: model.ItemEmprestado) -> None:
        self._items.add(item)

    def get(self, id_item: str) -> model.ItemEmprestado:
        for item in self._items:
            if item.id_item == id_item:
                return item
        raise ItemNaoEncontrado(id_item)

    def list(self) -> list[model.ItemEmprestado]:
        return list(self._items)