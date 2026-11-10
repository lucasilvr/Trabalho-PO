from biblioteca.acervo.domain import model
from biblioteca.acervo.adapters.repository import AbstractRepository


def _normalizar_texto(valor: str, nome_campo: str) -> str:
    texto = (valor or "").strip()
    if not texto:
        raise ValueError(f"{nome_campo} não pode ser vazio.")
    return texto


def adicionar_livro(isbn: str, titulo: str, autor: str, repo: AbstractRepository, session):
    isbn_normalizado = _normalizar_texto(isbn, "ISBN")
    titulo_normalizado = _normalizar_texto(titulo, "Título")
    autor_normalizado = _normalizar_texto(autor, "Autor")

    livro = model.Livro(
        isbn=isbn_normalizado,
        titulo=titulo_normalizado,
        autor=autor_normalizado,
    )
    repo.add(livro)
    session.commit()
    return livro


def listar_livros(repo: AbstractRepository):
    return repo.list()


def inativar_livro(isbn: str, repo: AbstractRepository, session):
    isbn_normalizado = _normalizar_texto(isbn, "ISBN")
    livro = repo.get(isbn_normalizado)
    if not livro:
        raise ValueError(f"Livro com ISBN {isbn_normalizado} não encontrado.")

    livro.inativar()
    session.commit()
    return livro