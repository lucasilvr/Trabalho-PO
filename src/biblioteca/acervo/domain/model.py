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

    def pode_ser_inativado(self) -> bool:
        return not any(exemplar.status == "emprestado" for exemplar in self.exemplares)

    def validar_inativacao(self):
        if not self.pode_ser_inativado():
            raise Exception(
                f"O livro '{self.titulo}' não pode ser inativado pois possui alguns livros emprestados."
            )

    def inativar(self):
        self.validar_inativacao()
        self.ativo = False