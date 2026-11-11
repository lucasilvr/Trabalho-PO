from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from biblioteca.multas.domain import model
from biblioteca.multas.domain.exceptions import MultaNaoEncontrada

class AbstractMultaRepository(ABC):
    @abstractmethod
    def add(self, multa: model.Multa) -> None:
        pass

    @abstractmethod
    def get(self, id_multa: str) -> model.Multa:
        """Deve levantar MultaNaoEncontrada quando o registro nao existir."""
        pass

    @abstractmethod
    def list(self) -> List[model.Multa]:
        pass

class SqlAlchemyMultaRepository(AbstractMultaRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, multa: model.Multa) -> None:
        self.session.add(multa)

    def get(self, id_multa: str) -> model.Multa:
        try:
            return self.session.query(model.Multa).filter_by(id_multa=id_multa).one()
        except NoResultFound as exc:
            raise MultaNaoEncontrada(id_multa) from exc

    def list(self) -> List[model.Multa]:
        return self.session.query(model.Multa).all()

class FakeMultaRepository(AbstractMultaRepository):
    def __init__(self, multas: List[model.Multa] = None):
        self._multas = multas or []

    def add(self, multa: model.Multa) -> None:
        self._multas.append(multa)

    def get(self, id_multa: str) -> model.Multa:
        for m in self._multas:
            if m.id_multa == id_multa:
                return m
        raise MultaNaoEncontrada(id_multa)

    def list(self) -> List[model.Multa]:
        return list(self._multas)