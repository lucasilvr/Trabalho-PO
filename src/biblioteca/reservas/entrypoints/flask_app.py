from datetime import datetime
from flask import Flask, jsonify, request
from biblioteca.reservas.adapters.repository import SqlAlchemyFilaEsperaRepository
from biblioteca.reservas.service_layer import services

def create_app(session):
    app = Flask(__name__)

    @app.route("/reservas", methods=["POST"])
    def reservar_livro_endpoint():
        repo = SqlAlchemyFilaEsperaRepository(session)
        try:
            reserva = services.reservar_livro(
                request.json["id_reserva"],
                request.json["id_leitor"],
                request.json["id_livro"],
                datetime.fromisoformat(request.json["data_reserva"]),
                repo,
                session,
            )
        except KeyError:
            return jsonify({"message": "Dados incompletos"}), 400
        return jsonify({"id_reserva": reserva.id_reserva, "status": reserva.status}), 201

    @app.route("/filas/<id_livro>/devolucao", methods=["POST"])
    def registrar_devolucao_endpoint(id_livro):
        repo = SqlAlchemyFilaEsperaRepository(session)
        try:
            fila = services.registrar_devolucao(
                id_livro, datetime.fromisoformat(request.json["data_hora"]), repo, session
            )
        except services.FilaNaoEncontrada as e:
            return jsonify({"message": str(e)}), 404
        return jsonify({"reservas": [{"id_reserva": r.id_reserva, "status": r.status} for r in fila.reservas]}), 200

    @app.route("/filas/<id_livro>/atualizacao", methods=["POST"])
    def atualizar_fila_endpoint(id_livro):
        repo = SqlAlchemyFilaEsperaRepository(session)
        try:
            fila = services.atualizar_fila(
                id_livro, datetime.fromisoformat(request.json["data_hora_atual"]), repo, session
            )
        except services.FilaNaoEncontrada as e:
            return jsonify({"message": str(e)}), 404
        return jsonify({"reservas": [{"id_reserva": r.id_reserva, "status": r.status} for r in fila.reservas]}), 200

    return app
