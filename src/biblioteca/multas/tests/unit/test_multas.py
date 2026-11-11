import pytest
from datetime import date
from biblioteca.multas.domain.model import (
    Multa, Pagamento, CalculoMultaBase, DecoradorJurosMora, DecoradorTaxaAdministrativa
)
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

def test_decorador_juros_mora_aplica_10_porcento_apos_5_dias():
    calculo = DecoradorJurosMora(CalculoMultaBase())
    multa = Multa("M3", "L3", 10, 2.0, calculo=calculo)
    assert multa.valor_total == 22.0  # (10 * 2.0) * 1.10 = 22.0

def test_decoradores_aninhados_juros_e_taxa_administrativa():
    calculo_composto = DecoradorTaxaAdministrativa(DecoradorJurosMora(CalculoMultaBase()))
    multa = Multa("M4", "L4", 10, 2.0, calculo=calculo_composto)
    assert multa.valor_total == 27.0  # ((10 * 2.0) * 1.10) + 5.0 = 27.0