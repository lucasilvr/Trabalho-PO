from datetime import date

from flask import Flask, jsonify, request
from sqlalchemy.orm.exc import NoResultFound

from biblioteca.emprestimo.adapters.repository import SqlAlchemyRepository
from biblioteca.emprestimo.service_layer import services


def create_app(session):
    app = Flask(__name__)

    def repository():
        return SqlAlchemyRepository(session)

    def item_to_dict(item):
        return {
            "id_item": item.id_item,
            "id_exemplar": item.id_exemplar,
            "data_emprestimo": item.data_emprestimo.isoformat(),
            "data_prevista_devolucao": (
                item.data_prevista_devolucao.isoformat()
            ),
            "data_devolucao": (
                item.data_devolucao.isoformat()
                if item.data_devolucao is not None
                else None
            ),
        }

    @app.post("/emprestimos")
    def registrar_emprestimo():
        dados = request.get_json(silent=True)

        if not dados:
            return jsonify({"erro": "JSON inválido"}), 400

        campos_obrigatorios = [
            "id_item",
            "id_exemplar",
            "data_emprestimo",
            "data_prevista_devolucao",
        ]

        if any(campo not in dados for campo in campos_obrigatorios):
            return jsonify({"erro": "Campos obrigatórios ausentes"}), 400

        try:
            data_emprestimo = date.fromisoformat(
                dados["data_emprestimo"]
            )
            data_prevista_devolucao = date.fromisoformat(
                dados["data_prevista_devolucao"]
            )
        except (TypeError, ValueError):
            return jsonify({"erro": "Data inválida"}), 400

        item = services.registrar_emprestimo(
            repo=repository(),
            id_item=dados["id_item"],
            id_exemplar=dados["id_exemplar"],
            data_emprestimo=data_emprestimo,
            data_prevista_devolucao=data_prevista_devolucao,
        )

        session.commit()

        return jsonify(item_to_dict(item)), 201

    @app.post("/emprestimos/<id_item>/devolucao")
    def registrar_devolucao(id_item):
        dados = request.get_json(silent=True)

        if not dados or "data_devolucao" not in dados:
            return jsonify(
                {"erro": "Data de devolução obrigatória"}
            ), 400

        try:
            data_devolucao = date.fromisoformat(
                dados["data_devolucao"]
            )
        except (TypeError, ValueError):
            return jsonify({"erro": "Data inválida"}), 400

        try:
            item = services.registrar_devolucao(
                repo=repository(),
                id_item=id_item,
                data_devolucao=data_devolucao,
            )
        except NoResultFound:
            return jsonify({"erro": "Item não encontrado"}), 404

        session.commit()

        return jsonify(item_to_dict(item)), 200

    @app.get("/emprestimos/<id_item>/atraso")
    def consultar_atraso(id_item):
        data_referencia = request.args.get("data_referencia")

        if not data_referencia:
            return jsonify(
                {"erro": "Data de referência obrigatória"}
            ), 400

        try:
            data = date.fromisoformat(data_referencia)
        except ValueError:
            return jsonify({"erro": "Data inválida"}), 400

        try:
            atrasado = services.consultar_atraso(
                repo=repository(),
                id_item=id_item,
                data_referencia=data,
            )
        except NoResultFound:
            return jsonify({"erro": "Item não encontrado"}), 404

        return jsonify(
            {
                "id_item": id_item,
                "atrasado": atrasado,
            }
        ), 200

    return app