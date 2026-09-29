from flask import request, jsonify
from datetime import date
from biblioteca.service_layer import services
from biblioteca.adapters import repository

@app.route("/multas/<id_multa>/pagar", methods=["POST"])
def endpoint_pagar_multa(id_multa):
    session = get_session()
    repo = repository.SqlAlchemyMultaRepository(session)
    data = request.json
    
    try:
        services.pagar_multa(id_multa, data['valor'], date.fromisoformat(data['data']), repo, session)
        return jsonify({"message": "Pagamento efetuado!"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400