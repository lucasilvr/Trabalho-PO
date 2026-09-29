import uuid
from dataclasses import dataclass, field
from datetime import date

@dataclass(frozen=True)
class CategoriaLeitor:
    nome: str
    limite_emprestimos: int

@dataclass
class Leitor:
    nome: str
    email: str
    categoria: CategoriaLeitor
    id_leitor: str = field(default_factory=lambda: str(uuid.uuid4()))
    emprestimos_ativos: int = 0
    ativo: bool = True
    data_cadastro: date = field(default_factory=date.today)

    def pode_emprestar(self) -> bool:
        return self.ativo and self.emprestimos_ativos < self.categoria.limite_emprestimos

    def registrar_emprestimo(self):
        if not self.ativo:
            raise ValueError("Leitor inativo não pode realizar empréstimos.")
        
        if not self.pode_emprestar():
            raise ValueError(
                f"Limite de {self.categoria.limite_emprestimos} empréstimos "
                f"atingido para a categoria {self.categoria.nome}."
            )
        
        self.emprestimos_ativos += 1

    def devolver_emprestimo(self):
        if self.emprestimos_ativos > 0:
            self.emprestimos_ativos -= 1

    def desativar(self):
        self.ativo = False

    def ativar(self):
        self.ativo = True