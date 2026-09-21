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
                raise Exception(f"O livro '{self.titulo}' não pode ser inativado pois possui alguns livros emprestados.")
        self.ativo = False