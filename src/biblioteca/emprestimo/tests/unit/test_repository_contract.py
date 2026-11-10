import pytest

from biblioteca.emprestimo.adapters.repository import FakeRepository
from biblioteca.emprestimo.domain.exceptions import ItemNaoEncontrado


def test_fake_repository_levanta_item_nao_encontrado():
    repo = FakeRepository([])

    with pytest.raises(ItemNaoEncontrado) as excinfo:
        repo.get("ITEM-404")

    assert excinfo.value.id_item == "ITEM-404"
