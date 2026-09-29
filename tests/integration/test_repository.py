from src.biblioteca.adapters.repository import SqlAlchemyRepository

def test_salvar_e_buscar_ordem_servico(session, ordem_servico):
    repo = SqlAlchemyRepository(session)

    ordem = ordem_servico("OS-001")

    repo.add(ordem)
    session.commit()

    ordem_busca = repo.get("OS-001")

    assert ordem_busca.id_ordem == ordem.id_ordem
    assert ordem_busca.laudo.id_laudo == ordem.laudo.id_laudo

def test_listar_ordens_servico(session, ordem_servico):
    repo = SqlAlchemyRepository(session)

    ordem1 = ordem_servico("OS-001")
    ordem2 = ordem_servico("OS-002")

    repo.add(ordem1)
    repo.add(ordem2)
    session.commit()

    ordens_listadas = repo.list()

    assert len(ordens_listadas) == 2
    assert {ordem.id_ordem for ordem in ordens_listadas} == {"OS-001", "OS-002"}