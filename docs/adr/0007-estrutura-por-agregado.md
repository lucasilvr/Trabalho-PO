# ADR 0007 — Organizar o pacote por agregado em vez de uma estrutura única

- **Status:** Aceita
- **Autor:** João Vicente Piller Menezes
- **Data:** 17/11/2026 (registra uma decisão adotada pelo grupo na Fase 1, em setembro de 2026)

## Contexto

O enunciado pede a estrutura do Apêndice B do livro-texto: um único pacote
`src/<pacote>/` com `domain/model.py`, `adapters/orm.py`, `adapters/repository.py`,
`service_layer/services.py` e `entrypoints/flask_app.py`, e os testes em uma pasta
`tests/` na raiz, separados em `unit/`, `integration/` e `e2e/`.

O grupo tem seis integrantes, cada um responsável por um agregado, e a avaliação
individual depende da autoria dos commits nos arquivos de cada agregado. Durante a
Fase 1, com todos editando os mesmos arquivos (por exemplo, um único `model.py` e um
único `orm.py`), os merges geraram conflitos frequentes. Um exemplo é o merge
`8e5972d`, que precisou resolver conflitos em `DECISIONS.md` e em
`src/biblioteca/domain/model.py`.

## Decisão

Manter as mesmas camadas do Apêndice B, mas repeti-las dentro de um subpacote por
agregado:

```
src/biblioteca/<agregado>/
├── domain/            (model.py)
├── adapters/          (orm.py, repository.py)
├── service_layer/     (services.py)
├── entrypoints/       (flask_app.py)
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

Os agregados são `acervo`, `cadastro`, `emprestimo`, `manutencao`, `multas` e `reservas`.
A CI executa as três camadas de teste de todos os agregados com
`pytest src/biblioteca/*/tests/unit`, `.../integration` e `.../e2e`, e o `pytest.ini`
da raiz usa `--import-mode=importlib` para permitir arquivos de teste com o mesmo nome
em agregados diferentes.

## Alternativas consideradas

1. **Apêndice B literal, com um único `model.py`, `orm.py`, `services.py` e
   `flask_app.py`:** é a estrutura esperada pela verificação automática, mas
   concentraria o código dos seis integrantes nos mesmos arquivos, aumentando os
   conflitos de merge e misturando a autoria de cada agregado em um mesmo arquivo.
2. **Um repositório ou serviço separado por agregado:** daria independência total,
   mas fugiria do escopo da disciplina (um único sistema em um único repositório) e
   exigiria integração entre serviços.
3. **Camadas do Apêndice B repetidas por agregado (escolhida):** preserva a separação
   em camadas e a direção das dependências pedidas pelo livro-texto, e deixa cada
   agregado em arquivos próprios.

## Consequências

### Positivas

- Cada integrante trabalha em arquivos do próprio agregado, o que reduz conflitos e
  deixa a autoria de cada arquivo clara no histórico.
- As camadas e a direção das dependências continuam as do Apêndice B: o domínio de
  cada agregado não importa SQLAlchemy nem Flask.
- Cada agregado pode ser testado isoladamente (`pytest src/biblioteca/reservas`).

### Negativas

- A estrutura não corresponde literalmente ao Apêndice B, o que pode afetar a
  verificação estrutural automática.
- Há repetição: cada agregado tem o seu próprio `orm.py`, `repository.py` e
  `flask_app.py`, e não existe um ponto único que monte a aplicação inteira.
- Cada agregado tem o seu próprio registro de mapeamento do SQLAlchemy, então regras
  que atravessam agregados ainda precisariam de uma composição comum.

## Evidências

- `8e5972d`: merge da Fase 1 com conflitos em arquivos compartilhados.
- `.github/workflows/ci.yml`: execução dos testes com `src/biblioteca/*/tests/<camada>`.
- `docs/retrospectiva.md` e `docs/arquitetura.md`: discutem o custo da repetição por
  agregado.
