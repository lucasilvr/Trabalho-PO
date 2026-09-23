from abc import ABC, abstractmethod

from src.biblioteca.domain import model


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, item: model.ItemEmprestado) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, id_item: str) -> model.ItemEmprestado:
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
        return (
            self.session.query(model.ItemEmprestado)
            .filter_by(id_item=id_item)
            .one()
        )

    def list(self) -> list[model.ItemEmprestado]:
        return self.session.query(model.ItemEmprestado).all()


class FakeRepository(AbstractRepository):
    def __init__(self, items):
        self._items = set(items)

    def add(self, item: model.ItemEmprestado) -> None:
        self._items.add(item)

    def get(self, id_item: str) -> model.ItemEmprestado:
        return next(
            item for item in self._items
            if item.id_item == id_item
        )

    def list(self) -> list[model.ItemEmprestado]:
        return list(self._items)