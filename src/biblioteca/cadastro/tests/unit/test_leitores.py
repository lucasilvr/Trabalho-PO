import pytest
from biblioteca.cadastro.domain.model import Leitor, CategoriaLeitor

def test_invariante_limite_emprestimos_por_categoria():
    categoria_aluno = CategoriaLeitor(nome="Aluno", limite_emprestimos=2)
    leitor = Leitor(nome="Isabella", email="isa@email.com", categoria=categoria_aluno)
    
    assert leitor.pode_fazer_emprestimo() is True
    
    leitor.emprestimos_ativos = 2
    
    assert leitor.pode_fazer_emprestimo() is False

def test_leitor_inativo_nao_pode_fazer_emprestimo():
    categoria_prof = CategoriaLeitor(nome="Professor", limite_emprestimos=5)
    leitor = Leitor(nome="Daniel", email="daniel@email.com", categoria=categoria_prof)
    
    leitor.inativar()
    
    assert leitor.pode_fazer_emprestimo() is False