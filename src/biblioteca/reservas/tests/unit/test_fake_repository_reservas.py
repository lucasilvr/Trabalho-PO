from biblioteca.reservas.adapters.repository import FakeFilaEsperaRepository
from biblioteca.reservas.domain.model import FilaEspera


def test_fake_repository_adiciona_busca_e_lista_filas():
    fila1 = FilaEspera("LIVRO-1")
    fila2 = FilaEspera("LIVRO-2")
    repo = FakeFilaEsperaRepository([])

    repo.add(fila1)
    repo.add(fila2)

    assert repo.get("LIVRO-1") is fila1
    assert repo.get("LIVRO-INEXISTENTE") is None
    assert {fila.id_livro for fila in repo.list()} == {"LIVRO-1", "LIVRO-2"}
