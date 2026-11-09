import pytest

from biblioteca.acervo.service_layer.validators import criar_cadeia_validacao_livro


def test_cadeia_valida_e_normaliza_todos_os_campos():
    cadeia = criar_cadeia_validacao_livro()

    resultado = cadeia.validar(
        {"isbn": "  123  ", "titulo": " Livro ", "autor": " Autor "}
    )

    assert resultado == {"isbn": "123", "titulo": "Livro", "autor": "Autor"}


@pytest.mark.parametrize(
    ("dados", "mensagem"),
    [
        ({"isbn": " ", "titulo": "Livro", "autor": "Autor"}, "ISBN"),
        ({"isbn": "123", "titulo": "", "autor": "Autor"}, "Título"),
        ({"isbn": "123", "titulo": "Livro", "autor": "  "}, "Autor"),
    ],
)
def test_cadeia_rejeita_campo_obrigatorio_vazio(dados, mensagem):
    cadeia = criar_cadeia_validacao_livro()

    with pytest.raises(ValueError, match=mensagem):
        cadeia.validar(dados)
