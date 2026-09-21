import pytest
from src.biblioteca.domain.model import Livro, Exemplar

def test_nao_deve_inativar_livro_emprestado():

    livro = Livro(isbn="1", titulo="1984", autor="George Orwell")
    exemplar_emprestado = Exemplar(id_exemplar="001", status="emprestado")
    livro.adicionar_exemplar(exemplar_emprestado)

    with pytest.raises(Exception, match="não pode ser inativado"):
        livro.inativar()

def test_deve_inativar_livro_quando_todos_exemplares_disponiveis():
    livro = Livro(isbn="1", titulo="1984", autor="George Orwell")
    exemplar_livre = Exemplar(id_exemplar="002", status="disponivel")
    livro.adicionar_exemplar(exemplar_livre)
    livro.inativar()
    assert livro.ativo is False