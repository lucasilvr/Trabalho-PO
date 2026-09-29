import pytest
import requests

BASE_URL = "http://localhost:5000"

def test_api_consegue_adicionar_livro():
    dados = {
        "isbn": "978-85-359-0277-8",
        "titulo": "Ensaio sobre a Cegueira",
        "autor": "José Saramago"
    }
    
    resposta = requests.post("/livros", json=dados)
    assert resposta.status_code == 201
    assert resposta.json()["status"] == "Livro adicionado com sucesso"

def test_api_consegue_inativar_livro():
    dados = {
        "isbn": "978-85-359-1484-9",
        "titulo": "O Conto da Aia",
        "autor": "Margaret Atwood"
    }
    requests.post("/livros", json=dados)
        
    resposta = requests.post("/livros/978-85-359-1484-9/inativar")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "Livro inativado com sucesso"
