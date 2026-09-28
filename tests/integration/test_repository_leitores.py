from biblioteca.domain import model
from biblioteca.adapters import repository
from sqlalchemy import text  

def test_repository_pode_salvar_um_leitor(session):
    categoria = model.CategoriaLeitor(nome="Aluno", limite_emprestimos=3)
    leitor = model.Leitor(nome="Isabella", email="isa@email.com", categoria=categoria)
    
    repo = repository.SqlAlchemyLeitorRepository(session)
    repo.add(leitor)
    session.commit()

    rows = session.execute(
        text("SELECT id_leitor, nome, email, categoria_nome FROM leitores")
    ).fetchall()
    
    assert len(rows) == 1
    assert rows[0].nome == "Isabella"