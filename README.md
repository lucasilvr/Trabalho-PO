# Sistema de Gestão de Biblioteca

Repositório do sistema desenvolvido para a disciplina de Projeto de Software.  
Stack: Python 3, Flask, SQLAlchemy e pytest.

## Equipe

Conforme as regras de avaliação da disciplina, a distribuição das responsabilidades técnicas (agregados/módulos) entre os integrantes do grupo está definida abaixo.

### Quem faz o quê

| Integrante | Agregado / Módulo | Pasta em `src/biblioteca/` | GitHub |
|---|---|---|---|
| Lucas Dias Silveira | Acervo (Catálogo) | `acervo/` | `@lucasilvr` |
| Sandy Fortes Cabral | Empréstimo | `emprestimo/` | `@SandyCabral` |
| João Vicente Piller Menezes | Reserva | `reservas/` | `@joaopiller` |
| Isabella Vieira da Motta | Cadastro de Leitores | `cadastro/` | `@isabellamott4` |
| Ana Laura Neuhaus Vega | Penalidades e Multas | `multas/` | `@ananeuhausv` |
| Karine Vitoria Marinho de Moraes | Manutenção e Restauro | `manutencao/` | `@kvmoraes` |

Para verificar os agregados previstos e qual integrante fica responsável por cada um acesse o arquivo `PROPOSTA.md`.
Para os autorrelatos e justificativas de projeto de cada fase, consulte o arquivo `DECISIONS.md`.

## Estrutura do repositório

O código fica em `src/biblioteca/`, com um subpacote por agregado. Cada agregado repete as camadas do Apêndice B do livro-texto (ver `docs/adr/0007-estrutura-por-agregado.md`):

```
src/biblioteca/<agregado>/
├── domain/          entidades, objetos de valor e regras de negócio
├── adapters/        mapeamento ORM e repositórios (real e fake)
├── service_layer/   casos de uso
├── entrypoints/     API Flask
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

Documentação da Fase 2, em `docs/`:

| Documento | Conteúdo |
|---|---|
| `docs/arquitetura.md` | Requisitos, estilos, trade-offs e alternativa (checkpoint 1) |
| `docs/adr/` | Architecture Decision Records, ao menos um por integrante |
| `docs/solid.md` | Refatorações SOLID (checkpoint 2) |
| `docs/gof.md` | Padrões GoF (checkpoint 3) |
| `docs/frameworks.md` | Análise dos frameworks (entrega final) |
| `docs/retrospectiva.md` | Retrospectiva da arquitetura (entrega final) |

## Como executar os testes

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest src/biblioteca/*/tests/unit
pytest src/biblioteca/*/tests/integration
pytest src/biblioteca/*/tests/e2e
```

São as mesmas três etapas executadas pela CI (`.github/workflows/ci.yml`). Para testar um único agregado: `pytest src/biblioteca/reservas`.
