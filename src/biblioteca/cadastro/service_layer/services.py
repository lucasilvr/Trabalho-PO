from biblioteca.cadastro.domain import model
from biblioteca.cadastro.adapters.repository import AbstractLeitorRepository

class CategoriaInvalida(Exception):
    pass

def cadastrar_leitor(nome: str, email: str, tipo_categoria: str, repo: AbstractLeitorRepository, session) -> str:
    limites = {"Aluno": 3, "Professor": 5}
    
    if tipo_categoria not in limites:
        raise CategoriaInvalida(f"Categoria {tipo_categoria} não permitida.")
        
    categoria = model.CategoriaLeitor(
        nome=tipo_categoria, 
        limite_emprestimos=limites[tipo_categoria]
    )
    
    leitor = model.Leitor(nome=nome, email=email, categoria=categoria)
    repo.add(leitor)
    session.commit()
    
    return leitor.id_leitor