from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from biblioteca.acervo.adapters import orm
from biblioteca.acervo.adapters import repository
from biblioteca.acervo.service_layer import services

app = Flask(__name__)
orm.start_mappers()
engine = create_engine('sqlite:///:memory:')
orm.metadata.create_all(engine)
get_session = sessionmaker(bind=engine)

@app.route("/livros", methods=["POST"])
def add_livro():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    dados = request.json
    try:
        services.adicionar_livro(
            dados['isbn'], dados['titulo'], dados['autor'], 
            repo, session
        )
        return jsonify({"status": "Livro adicionado com sucesso"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@app.route("/livros/<isbn>/inativar", methods=["POST"])
def inativar_livro(isbn):
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    
    try:
        services.inativar_livro(isbn, repo, session)
        return jsonify({"status": "Livro inativado com sucesso"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 400