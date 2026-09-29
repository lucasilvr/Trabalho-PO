import pytest

from src.biblioteca.domain.model import (
    OrdemServico, 
    OrdemServicoStatus
)

def test_criar_ordem_servico_com_status_aberta(ordem_servico):
    ordem = ordem_servico("OS-001")

    assert ordem.status == OrdemServicoStatus.ABERTA
    assert ordem.id_ordem == "OS-001"

def test_nao_criar_ordem_servico_com_dano_nao_reparavel(laudo_irreparavel):
    with pytest.raises(
        ValueError,
        match="Não é possível criar uma ordem de serviço para um dano não reparável."
    ):
        OrdemServico(
            id_ordem="OS-002",
            laudo=laudo_irreparavel,
            exemplar_disponivel=True    
        )