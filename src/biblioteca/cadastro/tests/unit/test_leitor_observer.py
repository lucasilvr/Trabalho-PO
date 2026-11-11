from biblioteca.cadastro.domain.model import CategoriaLeitor, Leitor, LeitorObserver

class MockEmailObserver(LeitorObserver):
    def __init__(self):
        self.notificado = False
        
    def leitor_inativado(self, leitor):
        self.notificado = True

def test_inativar_leitor_notifica_observers():
    categoria = CategoriaLeitor("Aluno", 3)
    leitor = Leitor(nome="Isa", email="isa@email.com", categoria=categoria)
    
    observer_email = MockEmailObserver()
    leitor.adicionar_observer(observer_email)
    
    # Ação
    leitor.inativar()
    
    # Validação
    assert leitor.ativo is False
    assert observer_email.notificado is True