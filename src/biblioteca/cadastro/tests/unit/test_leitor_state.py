from biblioteca.cadastro.domain import model

def test_transicao_de_estado_do_leitor_bloqueia_emprestimo():
    categoria = model.CategoriaLeitor("Aluno", 3)
    leitor = model.Leitor(nome="Isa", email="isa@email.com", categoria=categoria, ativo=True)
    
    # Estado inicial: Ativo
    assert leitor.pode_fazer_emprestimo() is True
    
    # Altera o estado
    leitor.inativar()
    
    # Novo estado: Inativo (barra o empréstimo imediatamente)
    assert leitor.pode_fazer_emprestimo() is False