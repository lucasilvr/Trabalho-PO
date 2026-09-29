from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from biblioteca.cadastro.adapters import orm
from biblioteca.cadastro.service_layer import services
from biblioteca.cadastro.adapters import repository

app = Flask(__name__)

engine = create_engine("sqlite:///:memory:")
orm.metadata.create_all(engine)
orm.start_mappers()
SessionLocal = sessionmaker(bind=engine)

@app.route("/leitores", methods=["POST"])
def cadastrar_leitor_endpoint():
 
    session = SessionLocal()
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
        session.close()
        return jsonify({"message": str(e)}), 400
    except KeyError:
        session.close()
        return jsonify({"message": "Dados incompletos"}), 400
        
    session.close()
    return jsonify({"id_leitor": leitor_id}), 201