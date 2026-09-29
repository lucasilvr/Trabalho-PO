from src.biblioteca.manutencao.service_layer.services import OrdemServicoService
from src.biblioteca.manutencao.adapters.repository import FakeRepository


def test_criar_ordem_servico(laudo_reparavel):

    repo = FakeRepository([])

    service = OrdemServicoService(repo)

    ordem = service.criar_ordem_servico(
        id_ordem="OS-001",
        laudo=laudo_reparavel,
        exemplar_disponivel=True
    )

    assert ordem.id_ordem == "OS-001"
    assert len(repo.list()) == 1