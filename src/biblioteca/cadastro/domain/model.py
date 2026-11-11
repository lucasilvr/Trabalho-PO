import abc
import uuid
import datetime

class CategoriaLeitor:
    def __init__(self, nome: str, limite_emprestimos: int):
        self.nome = nome
        self.limite_emprestimos = limite_emprestimos

    def __composite_values__(self):
        return self.nome, self.limite_emprestimos


class LeitorObserver(abc.ABC):
    @abc.abstractmethod
    def leitor_inativado(self, leitor):
        pass


class Leitor:
    def __init__(self, nome: str, email: str, categoria: CategoriaLeitor, id_leitor: str = None, emprestimos_ativos: int = 0, ativo: bool = True, data_cadastro = None):
        self.id_leitor = id_leitor or str(uuid.uuid4())
        self.nome = nome
        self.email = email
        self.categoria = categoria
        self.emprestimos_ativos = emprestimos_ativos
        self.ativo = ativo
        self.data_cadastro = data_cadastro or datetime.date.today()

    @property
    def observers(self):
        if not hasattr(self, '_observers'):
            self._observers = []
        return self._observers

    def adicionar_observer(self, observer: LeitorObserver):
        self.observers.append(observer)

    def pode_fazer_emprestimo(self) -> bool:
        if not self.ativo:
            return False
        return self.emprestimos_ativos < self.categoria.limite_emprestimos
        
    def inativar(self):
        self.ativo = False
        for obs in self.observers:
            obs.leitor_inativado(self)

class FabricaCategoriaLeitor:
    @staticmethod
    def criar(tipo_categoria: str) -> CategoriaLeitor:
        tipo = tipo_categoria.strip().lower()
        if tipo == "aluno":
            return CategoriaLeitor(nome="Aluno", limite_emprestimos=3)
        elif tipo == "professor":
            return CategoriaLeitor(nome="Professor", limite_emprestimos=5)
        
        # Caso padrão se a categoria não for reconhecida
        return CategoriaLeitor(nome=tipo_categoria, limite_emprestimos=1)
