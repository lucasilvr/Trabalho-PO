from src.biblioteca.domain import model
from src.biblioteca.adapters.repository import AbstractRepository

def adicionar_livro(isbn: str, titulo: str, autor: str, repo: AbstractRepository, session):
    livro = model.Livro(isbn=isbn, titulo=titulo, autor=autor)
    repo.add(livro)
    session.commit()

def inativar_livro(isbn: str, repo: AbstractRepository, session):
    livro = repo.get(isbn)
    if not livro:
        raise ValueError(f"Livro com ISBN {isbn} não encontrado.")
    
    livro.inativar()
    session.commit()