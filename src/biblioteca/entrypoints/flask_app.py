from flask import Flask, request, jsonify, session
from biblioteca.service_layer import services
from biblioteca.adapters import repository, orm

app = Flask(__name__)

@app.route("/leitores", methods=["POST"])
def cadastrar_leitor_endpoint():
    # session viria do setup do banco da equipe
    repo = repository.SqlAlchemyLeitorRepository(session) 
    
    try:
        leitor_id = services.cadastrar_leitor(
            nome=request.json["nome"],
            email=request.json["email"],
            tipo_categoria=request.json["tipo_categoria"],
            repo=repo,
            session=session
        )
    except services.CategoriaInvalida as e:
        return jsonify({"message": str(e)}), 400
    except KeyError:
        return jsonify({"message": "Dados incompletos"}), 400
        
    return jsonify({"id_leitor": leitor_id}), 201