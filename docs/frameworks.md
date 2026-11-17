# Frameworks na solução Biblioteca

Este documento analisa os três frameworks usados no sistema: **Flask** (interface HTTP),
**SQLAlchemy** (persistência) e **pytest** (testes). Para cada um, descrevemos o papel na
solução, a camada em que aparece e por que o domínio não depende dele. Em seguida,
localizamos os pontos de inversão de controle no código do grupo e os padrões de projeto
que os frameworks usam internamente. Por fim, comparamos com uma solução full-stack
como o Django.

## 1. Panorama

| Framework | Papel na solução | Onde aparece | Direção da dependência |
|---|---|---|---|
| Flask | Receber HTTP, rotear e montar a resposta | `src/biblioteca/*/entrypoints/flask_app.py` | A aplicação cria o `Flask`, mas é o Flask que chama as views |
| SQLAlchemy | Mapear objetos para tabelas e controlar a sessão | `src/biblioteca/*/adapters/orm.py` e `repository.py` | A aplicação descreve o mapa; o SQLAlchemy reconstrói e persiste os objetos |
| pytest | Descobrir, executar e injetar dependências nos testes | `src/biblioteca/*/tests/` | O pytest chama as funções de teste e injeta as fixtures |

As dependências estão declaradas em `requirements.txt` (`flask`, `sqlalchemy`, `pytest`,
`requests`), sem versões fixadas. A CI usa Python 3.12 (`.github/workflows/ci.yml`).

## 2. Flask

### Papel e camada

O Flask é o **adapter de entrada**. Ele recebe a requisição HTTP, identifica a rota,
converte o corpo em dados acessíveis (`request.get_json`), executa a função de view e
serializa a resposta (`jsonify`). No nosso código, os views ficam em
`entrypoints/flask_app.py` e apenas orquestram: leem a entrada, chamam o serviço e
devolvem status HTTP.

No agregado Empréstimo, `create_app(session)` (`flask_app.py:10`) recebe a sessão já
criada e devolve a aplicação configurada. Os três endpoints são:

- `@app.post("/emprestimos")` (`flask_app.py:32`);
- `@app.post("/emprestimos/<id_item>/devolucao")`;
- `@app.get("/emprestimos/<id_item>/atraso")`.

No agregado Acervo (`src/biblioteca/acervo/entrypoints/flask_app.py`), a aplicação expõe
os endpoints de catálogo:

- `@app.route("/livros", methods=["POST"])` (`flask_app.py:14`) — lê `request.json`,
  delega a criação e validação para `services.adicionar_livro(...)` e devolve HTTP 201;
- `@app.route("/livros/<isbn>/inativar", methods=["POST"])` (`flask_app.py:28`) — recebe
  o `<isbn>` extraído da rota pelo Flask, chama `services.inativar_livro(isbn, repo, session)`
  e traduz erros de busca (`ValueError` → HTTP 404) e de regra de negócio (`Exception` →
  HTTP 400) em respostas JSON com `jsonify`.

### Por que o domínio não depende do Flask

O domínio não importa Flask em nenhum arquivo. A verificação é direta:

```text
git grep -n -i -E "flask|sqlalchemy|pytest" -- "src/biblioteca/*/domain/**"
```

O único resultado é um **comentário** em `emprestimo/domain/model.py` que menciona o
SQLAlchemy; não há import. Já os imports de Flask aparecem somente nos seis
`entrypoints/flask_app.py`. Isso é consequência da direção das dependências:
entrypoint → serviço → domínio. O domínio é Python puro (`ItemEmprestado`, `Reserva`,
`Livro`, `Exemplar`, `Leitor`, `Multa`) e pode ser testado sem servidor HTTP — por
exemplo, a regra `Livro.pode_ser_inativado()` e `Livro.inativar()` em
`acervo/domain/model.py` é exercitada diretamente em `acervo/tests/unit/test_acervo.py`
sem instanciar o Flask.

## 3. SQLAlchemy

### Papel e camada

O SQLAlchemy é o **adapter de persistência**. Ele aparece em dois pontos:

- `adapters/orm.py`: define as tabelas (`Table`, `registry`) e liga cada tabela à classe
  de domínio com `map_imperatively`;
- `adapters/repository.py`: encapsula a `Session` por trás de `AbstractRepository`.

O padrão Repository é o que impede o resto do sistema de conhecer a `Session`. O serviço
depende de `AbstractRepository`; o entrypoint monta `SqlAlchemyRepository(session)` no
ponto de composição; os testes de unidade usam `FakeRepository`.

### Por que o domínio não depende do SQLAlchemy

As entidades **não herdam** de `declarative_base` nem de `Model`. O mapeamento é externo
e imperativo:

```python
# src/biblioteca/emprestimo/adapters/orm.py:23
def start_mappers():
    mapper_registry.map_imperatively(
        model.ItemEmprestado,
        itens_emprestados,
    )
```

No agregado Acervo (`src/biblioteca/acervo/adapters/orm.py:31-46`), o mapeamento
imperativo também liga a raiz de agregado `Livro` e a entidade interna `Exemplar` às
tabelas `livros` e `exemplares`, configurando o relacionamento `1:N` externamente sem
que `Livro` ou `Exemplar` importem qualquer classe do SQLAlchemy:

```python
# src/biblioteca/acervo/adapters/orm.py:37-46
linhas_mapper = mapper_registry.map_imperatively(model.Exemplar, exemplares)
mapper_registry.map_imperatively(
    model.Livro,
    livros,
    properties={
        "exemplares": relationship(
            linhas_mapper,
            collection_class=list,
        )
    },
)
```

Isso mantém `ItemEmprestado`, `Livro` e `Exemplar` como classes comuns (`self.exemplares: List[Exemplar] = []` no construtor de `Livro`) e permite que o mesmo domínio seja
testado com um repositório em memória (`FakeRepository` e `DummySession` em
`acervo/tests/unit/test_services_acervo.py`). Além disso, no Empréstimo o repositório traduz a exceção do
framework para uma exceção de domínio: `SqlAlchemyRepository.get` converte
`NoResultFound` em `ItemNaoEncontrado` (`repository.py:42-43`), de modo que a camada HTTP
não precisa importar nada do SQLAlchemy.

## 4. pytest

### Papel e camada

O pytest não faz parte da aplicação em execução; ele é a infraestrutura de testes. A
suíte é dividida em três camadas, e a CI executa cada uma separadamente
(`.github/workflows/ci.yml`):

- `tests/unit` — domínio, validadores e serviços com `FakeRepository` (por exemplo, `acervo/tests/unit/test_acervo.py`, `test_services_acervo.py` e `test_validators.py`);
- `tests/integration` — repositórios e mapeamento com SQLite em memória (por exemplo, `acervo/tests/integration/test_repository.py` e `emprestimo/tests/integration/test_emprestimo_orm.py`);
- `tests/e2e` — a API pelo cliente de testes do Flask (por exemplo, `acervo/tests/e2e/test_api.py` e `emprestimo/tests/e2e/test_emprestimo_api.py`).

### Por que o domínio não depende do pytest

O domínio também não importa pytest. Os testes de unidade são funções comuns, com
`assert`, que recebem objetos de domínio por parâmetro; quem as executa é o pytest. Como
as asserções são `assert` puro e as fixtures são opcionais, a mesma suíte rodaria sob
`unittest` sem alterar o código de domínio. A dependência existe apenas na infraestrutura
de teste, não no modelo.

## 5. Inversão de controle no código do grupo

Inversão de controle (IoC) significa que **o framework chama o nosso código**, e não o
contrário. Localizamos quatro pontos concretos.

### 5.1 Registro de rotas e injeção de parâmetros de URL (Flask)

```python
# src/biblioteca/emprestimo/entrypoints/flask_app.py:32
@app.post("/emprestimos")
def registrar_emprestimo():
    ...

# src/biblioteca/acervo/entrypoints/flask_app.py:28
@app.route("/livros/<isbn>/inativar", methods=["POST"])
def inativar_livro(isbn):
    ...
```

O decorador não executa a view: ele registra a função no mapa de URLs da aplicação.
Quem chama `registrar_emprestimo()` ou `inativar_livro(isbn)` em produção é o Flask,
quando chega uma requisição `POST /emprestimos` ou `POST /livros/<isbn>/inativar`
(extraindo o segmento `<isbn>` da URL e passando-o como argumento para a função). O nosso
código nunca faz essa chamada diretamente — nos testes E2E quem dispara é
`client.post(...)`.

### 5.2 Ciclo de vida da requisição (Flask)

`request.get_json()` (ou `request.json` em `acervo/entrypoints/flask_app.py:18`),
`request.args` e `jsonify()` dependem do contexto de requisição que
o Flask cria e destrói. A view não recebe esses objetos como parâmetro; ela os encontra
no contexto que o framework preparou. Isso é IoC: o ciclo é do framework, e o nosso
código é chamado dentro dele.

### 5.3 Mapeamento objeto-relacional (SQLAlchemy)

Quando uma linha é carregada, o SQLAlchemy **instancia a nossa classe** e preenche os
atributos mapeados. Nós não escrevemos esse carregamento. A consequência aparece no
nosso domínio em dois pontos:

- Em Empréstimo, objetos reconstruídos pelo SQLAlchemy não passam pelo `__init__`, por isso
  `ItemEmprestado.politica_atraso` é uma property que reencontra a estratégia a partir da
  categoria persistida (`emprestimo/domain/model.py:24-34`).
- Em Acervo, o SQLAlchemy injeta o gerenciador `_sa_class_manager` nas classes `Livro` e
  `Exemplar` e popula a coleção `livro.exemplares` ao carregar do banco; por isso
  `start_mappers()` (`acervo/adapters/orm.py:32-35`) precisa verificar
  `getattr(model.Livro, "_sa_class_manager", None)` para não instrumentar a classe duas
  vezes entre execuções de teste.

Esses detalhes só existem porque o framework controla a construção e instrumentação do objeto.

### 5.4 Fixtures e parametrização (pytest)

```python
# src/biblioteca/emprestimo/tests/e2e/test_emprestimo_api.py:9
@pytest.fixture
def client():
    ...
    with app.test_client() as client:
        yield client

# src/biblioteca/acervo/tests/integration/test_repository.py:8
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    orm.metadata.create_all(engine)
    clear_mappers()
    orm.start_mappers()
    yield sessionmaker(bind=engine)()
    clear_mappers()
```

O teste declara `def test_api_registra_emprestimo(client)` ou
`def test_repository_can_save_a_livro(session)`, mas não chama `client()` nem `session()`:
o pytest descobre a fixture pelo nome, executa o setup (até o `yield`), injeta o valor,
chama a função de teste e depois retoma a fixture para o teardown (como o `clear_mappers()`
em Acervo). O mesmo vale para as fixtures `in_memory_db` e `session` em
`cadastro/tests/conftest.py` e `multas/tests/conftest.py`, e para
`@pytest.mark.parametrize` em `acervo/tests/unit/test_validators.py:16-28`, onde o pytest
invoca `test_cadeia_rejeita_campo_obrigatorio_vazio(dados, mensagem)` uma vez para cada
tupla configurada.

## 6. Framework ou biblioteca?

A diferença prática é a **direção da chamada**:

- **Biblioteca:** o nosso código chama a biblioteca e mantém o controle do fluxo.
- **Framework:** o framework chama o nosso código; nós preenchemos pontos de extensão
  (rotas, mapeamentos, fixtures) e ele executa o fluxo principal.

O mesmo pacote pode se comportar das duas formas. O SQLAlchemy é biblioteca quando
fazemos `create_engine(...)`, `session.query(...)` e `session.execute(text(...))`; é framework quando o mapper
reconstrói uma entidade (e suas coleções relacionadas, como `Livro.exemplares`) a partir de linhas do banco. O Flask é biblioteca quando
importamos `Flask` e montamos a aplicação; é framework quando o roteador
chama a view. O pytest é framework em todos os momentos relevantes: nós escrevemos testes
e fixtures, mas quem os descobre e executa é ele.

| Uso no nosso código | Quem chama quem | Classificação |
|---|---|---|
| `Flask(__name__)` em `flask_app.py` | nós chamamos o Flask | biblioteca |
| `@app.post("/emprestimos")` e `@app.route("/livros/<isbn>/inativar", ...)` | Flask chama a view | framework |
| `create_engine("sqlite:///:memory:")` e `session.execute(text(...))` | nós chamamos o SQLAlchemy | biblioteca |
| `map_imperatively(...)` e `relationship(...)` | SQLAlchemy instancia e popula as entidades | framework |
| `@pytest.fixture def client()` / `def session()` e `@pytest.mark.parametrize` | pytest injeta dependências e chama o teste | framework |

## 7. Padrões de projeto que os frameworks usam internamente

Os padrões abaixo são usados **pelos frameworks**, e cada um pode ser localizado no
código do grupo.

### 7.1 Decorator (Flask e pytest)

`@app.post("/emprestimos")` (`emprestimo/entrypoints/flask_app.py:32`) e
`@app.route("/livros", methods=["POST"])` (`acervo/entrypoints/flask_app.py:14,28`) são
decoradores que recebem a função de view (`registrar_emprestimo`, `add_livro`,
`inativar_livro`), registram a rota no `url_map` e devolvem a função. O mesmo mecanismo aparece em todos os
`entrypoints/flask_app.py`, além dos decoradores `@pytest.fixture` e
`@pytest.mark.parametrize` (`acervo/tests/unit/test_validators.py:16`) no pytest.

### 7.2 Registry (SQLAlchemy)

`mapper_registry = registry()` e `metadata` (`emprestimo/adapters/orm.py:7-8` e
`acervo/adapters/orm.py:5-6`) são um
registro: cada `Table(...)` se inscreve em `metadata` e cada `map_imperatively` inscreve a
classe de domínio (`ItemEmprestado`, `Livro`, `Exemplar`) no registry. É esse registro que o framework consulta para criar o
schema (`metadata.create_all(engine)`), para limpar os mapeamentos entre testes (`mapper_registry.dispose()` em `acervo/adapters/orm.py:27-28`) e para reconstruir objetos. O Flask tem o
equivalente em `app.url_map`, alimentado pelos decoradores de rota.

### 7.3 Strategy (roteamento do Flask/Werkzeug)

O mapa de URLs escolhe, para cada requisição, qual função de view executa. Os endpoints
`POST /emprestimos`, `POST /emprestimos/<id_item>/devolucao` e
`GET /emprestimos/<id_item>/atraso` (em Empréstimo), ou `POST /livros` e
`POST /livros/<isbn>/inativar` (em Acervo), são algoritmos intercambiáveis selecionados pelo
roteador; a view não decide se é chamada.

### 7.4 Unit of Work (SQLAlchemy)

A `Session` acumula as mudanças e decide quando emitir os comandos. No nosso código isso
aparece nos repositórios (`self.session.add(item)` em `emprestimo/adapters/repository.py` e
`self.session.add(livro)` em `acervo/adapters/repository.py:22`) e no
`session.commit()` chamado nos serviços (`acervo/service_layer/services.py:20,35`) ou entrypoints. Em `acervo/entrypoints/flask_app.py:12`, `get_session = sessionmaker(bind=engine)` usa ainda o padrão **Factory Method** do SQLAlchemy para fabricar uma nova unidade de trabalho (`Session`) a cada requisição.

### 7.5 Identity Map (SQLAlchemy)

Uma mesma linha carregada duas vezes na mesma sessão devolve o **mesmo objeto**. O nosso
teste `test_item_recarregado_do_banco_usa_politica_da_categoria`
(`emprestimo/tests/integration/test_emprestimo_orm.py`) usa `session.expunge_all()`
justamente para descartar o objeto em memória e forçar o carregamento do banco. Sem o
identity map, esse cuidado seria desnecessário.

### 7.6 Proxy (SQLAlchemy)

Os atributos mapeados são descritores instrumentados (`_sa_class_manager`): ao ler ou atribuir um campo (ou ao acessar a coleção `livro.exemplares` configurada via `relationship` em `acervo/adapters/orm.py:42-45`), o
SQLAlchemy intercepta o acesso e registra a mudança para o flush. A classe de domínio não contém esse código;
ele é gerado pelo mapeamento em `adapters/orm.py`.

### 7.7 Template Method (pytest)

O pytest define o esqueleto de coleta, setup, execução e teardown, e nós preenchemos
pontos variáveis: o nome `test_*`, os arquivos `conftest.py` e as fixtures. Em
`test_emprestimo_api.py` (fixture `client`) e em `acervo/tests/integration/test_repository.py:8-15` (fixture `session`), o `yield` da fixture marca exatamente a fronteira entre setup (`create_all`, `start_mappers`) e
teardown (`clear_mappers`) que o framework controla.

### 7.8 Composite (pytest)

A suíte é uma árvore (diretório → módulo → função) tratada de forma uniforme pelo runner.
É por isso que `pytest src/biblioteca/*/tests/unit` executa dezenas de testes de agregados
diferentes com o mesmo comando, sem que a CI conheça cada arquivo.

## 8. O que mudaria com Django

O Django é um framework **full-stack**: traz ORM, roteamento, views, templates, admin,
autenticação, migrações e configuração global no mesmo pacote. Usá-lo mudaria pontos
estruturais do projeto:

1. **Domínio acoplado.** As entidades herdariam de `models.Model`. `ItemEmprestado`,
   `Reserva`, `Livro` e `Exemplar` passariam a depender do framework, e a verificação
   `git grep` que hoje mostra o domínio limpo deixaria de valer. O mapeamento explícito
   de `adapters/orm.py` desapareceria em favor de campos declarados na própria classe
   (por exemplo, no Acervo, `self.exemplares: List[Exemplar] = []` deixaria de ser uma
   lista Python pura e viraria um `models.ForeignKey(Livro, related_name="exemplares")`
   atrelado ao `RelatedManager` do Django).
2. **Persistência via QuerySet.** Não haveria `AbstractRepository` nem
   `SqlAlchemyRepository`. O acesso seria por `Model.objects.filter(...)`, e o
   `FakeRepository` usado nos testes de unidade (`test_services_acervo.py`,
   `test_services_emprestimo.py`) precisaria ser substituído por mocks ou
   por um banco de teste. A refatoração de LSP/DIP do checkpoint 2 em Empréstimo (contrato
   único de `ItemNaoEncontrado`) e a checagem em memória `Livro.pode_ser_inativado()` em
   Acervo teriam de ser repensadas no vocabulário de `DoesNotExist` e `QuerySet` do Django.
3. **Roteamento e views.** As rotas sairiam dos decoradores e iriam para `urls.py`,
   apontando para views baseadas em função ou classe. Para JSON seria comum adicionar o
   Django REST Framework, mais uma dependência (onde o *Chain of Responsibility* de
   `ValidadorCampoLivro` no Acervo disputaria espaço com `Serializer` ou `Model.clean()`).
4. **Configuração e testes.** Entrariam `settings.py`, `manage.py`, `INSTALLED_APPS` e
   migrações geradas. Os testes precisariam de `pytest-django` e da fixture `db`, e o
   SQLite em memória montado à mão daria lugar ao banco de teste do Django.
5. **Ganhos.** Migrações automáticas, admin pronto, autenticação e menos código de
   ligação. Para um CRUD com muitas telas, seria mais rápido.
6. **Perdas.** O domínio deixaria de ser Python puro; o setup de teste ficaria mais
   pesado; e a separação que usamos na Fase 2 para refatorar SOLID e aplicar padrões GoF
   ficaria menos nítida, porque o framework passaria a ditar a forma das entidades.

Para este trabalho, que exige camadas explícitas, domínio testável sem infraestrutura e
refatorações localizadas, a combinação Flask + SQLAlchemy + pytest atende melhor. O
Django seria vantajoso se o objetivo fosse produtividade em CRUD e administração, ao
custo de maior acoplamento do domínio.

## 9. Evidências

- Domínio sem imports de framework: `git grep -n -i -E "flask|sqlalchemy|pytest" -- "src/biblioteca/*/domain/**"` (apenas um comentário).
- Imports de Flask restritos aos entrypoints: seis arquivos `entrypoints/flask_app.py`.
- Imports de SQLAlchemy concentrados em `adapters/orm.py`, `adapters/repository.py`, testes e nos entrypoints que montam o engine.
- Suítes separadas na CI: `unit`, `integration` e `e2e` (`.github/workflows/ci.yml`).
- Execução local em 17/11/2026: 63 testes unitários, 15 de integração e 20 E2E, todos passando.
