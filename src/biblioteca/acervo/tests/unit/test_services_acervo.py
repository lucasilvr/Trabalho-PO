import pytest

from biblioteca.acervo.adapters.repository import FakeRepository
from biblioteca.acervo.domain.model import Livro
from biblioteca.acervo.service_layer import services


class DummySession:
    def __init__(self):
        self.commits = 0

    def commit(self):
        self.commits += 1


def test_adicionar_livro_persiste_livro_no_repositorio():
    repo = FakeRepository([])
    session = DummySession()

    livro = services.adicionar_livro(
        isbn="978-85-359-0277-8",
        titulo="Ensaio sobre a Cegueira",
        autor="José Saramago",
        repo=repo,
        session=session,
    )

    assert livro is repo.get("978-85-359-0277-8")
    assert livro.titulo == "Ensaio sobre a Cegueira"
    assert session.commits == 1


def test_inativar_livro_altera_estado_do_livro():
    livro = Livro(isbn="978-85-359-1484-9", titulo="O Conto da Aia", autor="Margaret Atwood")
    repo = FakeRepository([livro])
    session = DummySession()

    resultado = services.inativar_livro(
        isbn="978-85-359-1484-9",
        repo=repo,
        session=session,
    )

    assert resultado is livro
    assert livro.ativo is False
    assert session.commits == 1


def test_inativar_livro_lanca_erro_quando_nao_existe():
    repo = FakeRepository([])
    session = DummySession()

    with pytest.raises(ValueError, match="não encontrado"):
        services.inativar_livro(
            isbn="978-85-359-0000-0",
            repo=repo,
            session=session,
        )
