from biblioteca.acervo.domain import model
from biblioteca.acervo.adapters.repository import AbstractRepository
from biblioteca.acervo.service_layer.validators import (
    criar_cadeia_validacao_isbn,
    criar_cadeia_validacao_livro,
)


def adicionar_livro(isbn: str, titulo: str, autor: str, repo: AbstractRepository, session):
    dados = criar_cadeia_validacao_livro().validar(
        {"isbn": isbn, "titulo": titulo, "autor": autor}
    )

    livro = model.Livro(
        isbn=dados["isbn"],
        titulo=dados["titulo"],
        autor=dados["autor"],
    )
    repo.add(livro)
    session.commit()
    return livro


def listar_livros(repo: AbstractRepository):
    return repo.list()


def inativar_livro(isbn: str, repo: AbstractRepository, session):
    dados = criar_cadeia_validacao_isbn().validar({"isbn": isbn})
    livro = repo.get(dados["isbn"])
    if not livro:
        raise ValueError(f"Livro com ISBN {dados['isbn']} não encontrado.")

    livro.inativar()
    session.commit()
    return livro