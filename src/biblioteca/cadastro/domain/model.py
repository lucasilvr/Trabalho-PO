import uuid
from dataclasses import dataclass, field
from datetime import date

class CategoriaLeitor:
    def __init__(self, nome: str, limite_emprestimos: int):
        self.nome = nome
        self.limite_emprestimos = limite_emprestimos

class FabricaCategoriaLeitor:
    @staticmethod
    def criar(tipo: str) -> CategoriaLeitor:
        limites = {"Aluno": 3, "Professor": 5}
        if tipo not in limites:
            raise ValueError(f"Categoria {tipo} não permitida.")
        return CategoriaLeitor(nome=tipo, limite_emprestimos=limites[tipo])

class Leitor:
    def __init__(self, nome: str, email: str, categoria: CategoriaLeitor, id_leitor: str = None, emprestimos_ativos: int = 0, ativo: bool = True, data_cadastro = None):
        import uuid
        import datetime
        self.id_leitor = id_leitor or str(uuid.uuid4())
        self.nome = nome
        self.email = email
        self.categoria = categoria
        self.emprestimos_ativos = emprestimos_ativos
        self.ativo = ativo
        self.data_cadastro = data_cadastro or datetime.date.today()

    def pode_fazer_emprestimo(self) -> bool:
        if not self.ativo:
            return False
        return self.emprestimos_ativos < self.categoria.limite_emprestimos