import pytest

from src.biblioteca.manutencao.domain.model import (
    OrdemServico, 
    OrdemServicoStatus
)

from src.biblioteca.manutencao.service_layer.commands import (
    ConcluirOrdemServicoCommand
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
            laudo=laudo_irreparavel
        )

def test_concluir_ordem_servico_com_command(ordem_servico):
    ordem = ordem_servico("OS-003")
    ordem.iniciar_execucao()

    comando = ConcluirOrdemServicoCommand(ordem)
    resultado = comando.execute()

    assert resultado.status == OrdemServicoStatus.CONCLUIDA
    assert resultado.id_ordem == "OS-003"


def test_command_nao_concluir_ordem_que_nao_esta_em_execucao(ordem_servico):
    ordem = ordem_servico("OS-004")

    comando = ConcluirOrdemServicoCommand(ordem)

    with pytest.raises(
        ValueError,
        match="A ordem de serviço só pode ser concluída se estiver em execução."
    ):
        comando.execute()

    assert ordem.status == OrdemServicoStatus.ABERTA