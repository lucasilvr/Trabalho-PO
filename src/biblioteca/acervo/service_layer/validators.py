class ValidadorCampoLivro:
    def __init__(self, campo: str, nome: str):
        self.campo = campo
        self.nome = nome
        self.proximo = None

    def definir_proximo(self, proximo: "ValidadorCampoLivro"):
        self.proximo = proximo
        return proximo

    def validar(self, dados: dict[str, str]) -> dict[str, str]:
        valor = dados.get(self.campo)
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{self.nome} não pode ser vazio.")

        dados_normalizados = dict(dados)
        dados_normalizados[self.campo] = valor.strip()
        if self.proximo is not None:
            return self.proximo.validar(dados_normalizados)
        return dados_normalizados


def criar_cadeia_validacao_livro() -> ValidadorCampoLivro:
    validar_isbn = ValidadorCampoLivro("isbn", "ISBN")
    validar_titulo = validar_isbn.definir_proximo(
        ValidadorCampoLivro("titulo", "Título")
    )
    validar_titulo.definir_proximo(ValidadorCampoLivro("autor", "Autor"))
    return validar_isbn


def criar_cadeia_validacao_isbn() -> ValidadorCampoLivro:
    return ValidadorCampoLivro("isbn", "ISBN")
