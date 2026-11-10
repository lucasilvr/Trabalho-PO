import abc
import uuid
import datetime
from dataclasses import dataclass
from typing import List

@dataclass
class Exemplar:
    id_exemplar: str
    status: str = "disponivel"

class Livro:
    def __init__(self, isbn: str, titulo: str, autor: str):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.exemplares: List[Exemplar] = []
        self.ativo = True

    def adicionar_exemplar(self, exemplar: Exemplar):
        self.exemplares.append(exemplar)

    def inativar(self):
        for exemplar in self.exemplares:
            if exemplar.status == "emprestado":
                raise Exception("O livro não pode ser inativado")
        self.ativo = False

class CategoriaLeitor:
    def __init__(self, nome: str, limite_emprestimos: int):
        self.nome = nome
        self.limite_emprestimos = limite_emprestimos

    
    def __composite_values__(self):
        return self.nome, self.limite_emprestimos

class FabricaCategoriaLeitor:
    @staticmethod
    def criar(tipo: str) -> CategoriaLeitor:
        limites = {"Aluno": 3, "Professor": 5}
        if tipo not in limites:
            raise ValueError(f"Categoria {tipo} não permitida.")
        return CategoriaLeitor(nome=tipo, limite_emprestimos=limites[tipo])

class EstadoLeitor(abc.ABC):
    @abc.abstractmethod
    def pode_fazer_emprestimo(self, leitor) -> bool:
        pass

class LeitorAtivo(EstadoLeitor):
    def pode_fazer_emprestimo(self, leitor) -> bool:
        return leitor.emprestimos_ativos < leitor.categoria.limite_emprestimos


class LeitorInativo(EstadoLeitor):
    def pode_fazer_emprestimo(self, leitor) -> bool:
        return False

class Leitor:
    def __init__(self, nome: str, email: str, categoria: CategoriaLeitor, id_leitor: str = None, emprestimos_ativos: int = 0, ativo: bool = True, data_cadastro = None):
        self.id_leitor = id_leitor or str(uuid.uuid4())
        self.nome = nome
        self.email = email
        self.categoria = categoria
        self.emprestimos_ativos = emprestimos_ativos
        self.data_cadastro = data_cadastro or datetime.date.today()
        
        self._estado = LeitorAtivo() if ativo else LeitorInativo()

    def pode_fazer_emprestimo(self) -> bool:
 
        return self._estado.pode_fazer_emprestimo(self)
        
    def inativar(self):
        
        self._estado = LeitorInativo()
        
    @property
    def ativo(self) -> bool:
       
        return isinstance(self._estado, LeitorAtivo)