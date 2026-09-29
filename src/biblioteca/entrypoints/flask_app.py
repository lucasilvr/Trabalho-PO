from datetime import date
from flask import Flask, request, jsonify

from src.biblioteca.domain import model
from src.biblioteca.adapters.repository import FakeRepository
from src.biblioteca.service_layer.services import OrdemServicoService

app = Flask(__name__)

repository = FakeRepository([])
service = OrdemServicoService(repository)

@app.post("/ordens-servico")
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

@app.get("/ordens-servico/<id_ordem>")
def buscar_ordem_servico(id_ordem):
    ordem_servico = service.buscar_ordem_servico(id_ordem)

    if ordem_servico is None:
        return jsonify(
            {"erro": "Ordem de servico nao encontrada"}
        ), 404

    return jsonify(
        {
            "id_ordem": ordem_servico.id_ordem,
            "status": ordem_servico.status.value,
            "id_laudo": ordem_servico.laudo.id_laudo
        }
    )

@app.post("/ordens-servico/<id_ordem>/iniciar")
def iniciar_ordem_servico(id_ordem):

    ordem_servico = service.executar_ordem_servico(id_ordem)

    return jsonify(
        {
            "id_ordem": ordem_servico.id_ordem,
            "status": ordem_servico.status.value
        }
    )

@app.post("/ordens-servico/<id_ordem>/concluir")
def concluir_ordem_servico(id_ordem):
    ordem_servico = service.concluir_ordem_servico(id_ordem)

    return jsonify(
        {
            "id_ordem": ordem_servico.id_ordem,
            "status": ordem_servico.status.value
        }
    )

@app.post("/ordens-servico/<id_ordem>/cancelar")
def cancelar_ordem_servico(id_ordem):
    ordem_servico = service.cancelar_ordem_servico(id_ordem)

    return jsonify(
        {
            "id_ordem": ordem_servico.id_ordem,
            "status": ordem_servico.status.value
        }
    )

@app.get("/ordens-servico")
def listar_ordens_servico():
    ordens = service.listar_ordens_servico()

    return jsonify(
        [
            {
                "id_ordem": ordem.id_ordem,
                "status": ordem.status.value
            }
            for ordem in ordens
        ]
    )

if __name__ == "__main__":
    app.run(debug=True)