import pytest
from datetime import date
from biblioteca.multas.domain.model import Multa, Pagamento
from biblioteca.multas.domain.exceptions import ValorPagamentoInvalido

def test_multa_muda_para_quitada_com_pagamento_exato():
    multa = Multa("M1", "L1", 2, 5.0)
    multa.registrar_pagamento(Pagamento(10.0, date.today()))
    assert multa.status == "Quitada"

def test_multa_continua_pendente_se_pagamento_insuficiente():
    multa = Multa("M2", "L2", 5, 2.0)
    multa.registrar_pagamento(Pagamento(5.0, date.today()))
    assert multa.status == "Pendente"

def test_pagamento_valor_invalido_dispara_excecao():
    with pytest.raises(ValorPagamentoInvalido):
        Pagamento(-10.0, date.today())

def test_pagamento_valor_zero_dispara_excecao():
    with pytest.raises(ValorPagamentoInvalido):
        Pagamento(0.0, date.today())