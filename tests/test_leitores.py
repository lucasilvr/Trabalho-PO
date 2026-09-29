import pytest
from biblioteca.domain.model import Leitor, CategoriaLeitor

def test_invariante_limite_emprestimos_por_categoria():
    categoria_aluno = CategoriaLeitor(nome="Aluno", limite_emprestimos=2)
    leitor = Leitor(nome="Isabella", email="isa@email.com", categoria=categoria_aluno)

    leitor.registrar_emprestimo()
    leitor.registrar_emprestimo()

    with pytest.raises(ValueError, match="Limite de 2 empréstimos atingido"):
        leitor.registrar_emprestimo()

def test_leitor_inativo_nao_pode_fazer_emprestimo():
    categoria_prof = CategoriaLeitor(nome="Professor", limite_emprestimos=5)
    leitor = Leitor(nome="Daniel", email="daniel@email.com", categoria=categoria_prof)
    
    leitor.desativar()
    
    with pytest.raises(ValueError, match="Leitor inativo não pode realizar empréstimos"):
        leitor.registrar_emprestimo()