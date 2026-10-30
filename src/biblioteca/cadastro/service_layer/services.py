from biblioteca.domain import model
from biblioteca.adapters.repository import AbstractLeitorRepository

class CategoriaInvalida(Exception):
    pass

def cadastrar_leitor(nome: str, email: str, tipo_categoria: str, repo: AbstractLeitorRepository, session) -> str:

    try:
        categoria = model.FabricaCategoriaLeitor.criar(tipo_categoria)
    except ValueError as e:
        raise CategoriaInvalida(str(e))
    
    leitor = model.Leitor(nome=nome, email=email, categoria=categoria)
    repo.add(leitor)
    session.commit()
    
    return leitor.id_leitor