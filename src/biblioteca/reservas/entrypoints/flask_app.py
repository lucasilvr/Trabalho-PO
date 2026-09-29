from datetime import datetime

from flask import Flask, jsonify, request

from biblioteca.reservas.adapters.repository import SqlAlchemyFilaEsperaRepository
from biblioteca.reservas.service_layer import services


def create_app(session):
    app = Flask(__name__)

    def repository():
        return SqlAlchemyFilaEsperaRepository(session)

    def reserva_to_dict(reserva):
        return {
            "id_reserva": reserva.id_reserva,
            "id_leitor": reserva.id_leitor,
            "id_livro": reserva.id_livro,
            "data_reserva": reserva.data_reserva.isoformat(),
            "status": reserva.status,
            "data_disponibilizacao": (
                reserva.data_disponibilizacao.isoformat()
                if reserva.data_disponibilizacao is not None
                else None
            ),
        }

    def fila_to_dict(fila):
        return {
            "id_livro": fila.id_livro,
            "reservas": [reserva_to_dict(r) for r in fila.reservas],
        }

    def ler_data_hora(dados, campo):
        if not dados or campo not in dados:
            return None
        try:
            return datetime.fromisoformat(dados[campo])
        except (TypeError, ValueError):
            return None

    @app.post("/reservas")
    def reservar_livro():
        dados = request.get_json(silent=True)

        if not dados:
            return jsonify({"erro": "JSON inválido"}), 400

        campos_obrigatorios = ["id_reserva", "id_leitor", "id_livro", "data_reserva"]

        if any(campo not in dados for campo in campos_obrigatorios):
            return jsonify({"erro": "Campos obrigatórios ausentes"}), 400

        data_reserva = ler_data_hora(dados, "data_reserva")
        if data_reserva is None:
            return jsonify({"erro": "Data inválida"}), 400

        reserva = services.reservar_livro(
            repo=repository(),
            id_reserva=dados["id_reserva"],
            id_leitor=dados["id_leitor"],
            id_livro=dados["id_livro"],
            data_reserva=data_reserva,
        )

        session.commit()

        return jsonify(reserva_to_dict(reserva)), 201

    @app.post("/filas/<id_livro>/devolucao")
    def registrar_devolucao_exemplar(id_livro):
        data_hora = ler_data_hora(request.get_json(silent=True), "data_hora")
        if data_hora is None:
            return jsonify({"erro": "Data e hora da devolução obrigatórias"}), 400

        try:
            fila = services.registrar_devolucao_exemplar(
                repo=repository(),
                id_livro=id_livro,
                data_hora=data_hora,
            )
        except services.FilaNaoEncontrada:
            return jsonify({"erro": "Fila de espera não encontrada"}), 404

        session.commit()

        return jsonify(fila_to_dict(fila)), 200

    @app.post("/filas/<id_livro>/atualizacao")
    def atualizar_fila(id_livro):
        data_hora_atual = ler_data_hora(request.get_json(silent=True), "data_hora_atual")
        if data_hora_atual is None:
            return jsonify({"erro": "Data e hora atual obrigatórias"}), 400

        try:
            fila = services.atualizar_fila(
                repo=repository(),
                id_livro=id_livro,
                data_hora_atual=data_hora_atual,
            )
        except services.FilaNaoEncontrada:
            return jsonify({"erro": "Fila de espera não encontrada"}), 404

        session.commit()

        return jsonify(fila_to_dict(fila)), 200

    @app.get("/filas/<id_livro>")
    def consultar_fila(id_livro):
        try:
            fila = services.consultar_fila(repo=repository(), id_livro=id_livro)
        except services.FilaNaoEncontrada:
            return jsonify({"erro": "Fila de espera não encontrada"}), 404

        return jsonify(fila_to_dict(fila)), 200

    return app
