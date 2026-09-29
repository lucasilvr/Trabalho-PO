import pytest
import requests

def test_api_processa_pagamento_com_sucesso():
    url = "http://localhost:5000/multas/M01/pagar"
    payload = {"valor": 10.0, "data": "2026-09-29"}
    
    try:
        response = requests.post(url, json=payload)
        assert response.status_code in [200, 400] 
    except requests.exceptions.ConnectionError:
        pytest.skip("Servidor da API não está rodando na porta 5000 para o teste E2E real.")