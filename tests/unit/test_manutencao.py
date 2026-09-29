from datetime import date

from src.biblioteca.domain.model import (
    OrdemServico, 
    LaudoAvaliacao, 
    OrdemServicoStatus
)

def test_criar_ordem_servico_com_status_aberta():
    # Arrange
    laudo = LaudoAvaliacao(
        id_laudo="LAUDO-001",
        id_item="ITEM-001",
        descricao_dano="Capa danificada",
        reparavel=True,
        data_avaliacao=date.today()
    )

    # Act
    ordem_servico = OrdemServico(
        id_ordem="ordem1",
        laudo=laudo,
        exemplar_disponivel=True
    )

    # Assert
    assert ordem_servico.status == OrdemServicoStatus.ABERTA

def test_nao_criar_ordem_servico_com_dano_nao_reparavel():
    # Arrange
    laudo = LaudoAvaliacao(
        id_laudo="LAUDO-002",
        id_item="ITEM-002",
        descricao_dano="Páginas rasgadas",
        reparavel=False,
        data_avaliacao=date.today()
    )

    # Act
    try:
        OrdemServico(
            id_ordem="ordem2",
            laudo=laudo,
            exemplar_disponivel=True    
        )

    # Assert
        assert False, "Deveria ter lançado ValueError para dano não reparável"

    except ValueError as e:
        assert str(e) == "Não é possível criar uma ordem de serviço para um dano não reparável."