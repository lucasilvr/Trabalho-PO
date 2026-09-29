from datetime import date
from flask import Flask, request, jsonify

from src.biblioteca.domain import model
from src.biblioteca.adapters.repository import FakeRepository
from src.biblioteca.service_layer.services import OrdemServicoService

app = Flask(__name__)

repository = FakeRepository([])
service = OrdemServicoService(repository)

@app.route("/ordens-servico", methods=["POST"])
def criar_ordem_servico():
    dados = request.get_json()

    laudo = model.LaudoAvaliacao(
        id_laudo=dados["id_laudo"],
        id_item=dados["id_item"],
        descricao_dano=dados["descricao_dano"],
        reparavel=dados["reparavel"],
        data_avaliacao=date.fromisoformat(
            dados["data_avaliacao"]
        )
    )

    ordem = service.criar_ordem_servico(
        id_ordem=dados["id_ordem"],
        laudo=laudo,
        exemplar_disponivel=dados["exemplar_disponivel"]
    )

    return jsonify(
        {
            "id_ordem": ordem.id_ordem,
            "status": ordem.status.value
        }
    ), 201

