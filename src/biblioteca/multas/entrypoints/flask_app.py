from flask import Flask, request, jsonify
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from biblioteca.multas.service_layer import services
from biblioteca.multas.adapters import orm, repository

app = Flask(__name__)
orm.start_mappers()
engine = create_engine("sqlite:///:memory:")
orm.metadata.create_all(engine)
get_session = sessionmaker(bind=engine)

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