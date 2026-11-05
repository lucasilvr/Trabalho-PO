# ADR 0001 — Separar o domínio da persistência

- **Status:** Aceita
- **Autora:** Sandy Fortes Cabral
- **Data:** 22/10/2026

## Contexto

O sistema Biblioteca tem entidades de domínio e operações de persistência. No módulo Empréstimo, `ItemEmprestado` contém os comportamentos `esta_atrasado()` e `registrar_devolucao()`. O mapeamento para tabelas fica em `src/biblioteca/adapters/orm.py`, e `src/biblioteca/adapters/repository.py` define `AbstractRepository`, `SqlAlchemyRepository` e `FakeRepository`.

Uma alternativa seria fazer a entidade herdar do modelo do ORM ou deixar a camada de serviço executar consultas SQLAlchemy diretamente. Isso aproximaria o código de negócio da infraestrutura e dificultaria testar suas regras isoladamente.

## Decisão

Manter o domínio independente de SQLAlchemy e Flask. O mapeamento clássico fica em `adapters/orm.py`; as operações de persistência passam pelo contrato `AbstractRepository`; os testes de serviço usam `FakeRepository`, enquanto os testes de integração usam a implementação real com SQLite.

## Alternativas consideradas

1. **Active Record:** a entidade seria também o modelo ORM e conheceria detalhes de persistência. É uma solução mais direta, mas aumenta o acoplamento e torna mais difícil substituir a infraestrutura ou testar o domínio isoladamente.
2. **Consultas SQLAlchemy dentro dos serviços:** reduz uma camada, mas faz cada caso de uso depender de `Session` e de detalhes do banco.
3. **Repository com mapeamento separado (escolhida):** exige interfaces, mapeamento e fake adicionais, mas deixa o domínio simples e permite trocar a implementação do repositório nos testes.

## Consequências

### Positivas

- Regras de domínio podem ser testadas sem banco de dados.
- A persistência fica concentrada em adapters.
- A mesma interface pode ser exercitada com fake e implementação real.
- Mudanças no mapeamento ORM não precisam alterar a entidade de domínio.

### Negativas

- Existem mais classes e arquivos para manter.
- O contrato abstrato, o fake e o repositório real precisam permanecer coerentes.
- A camada de entrada ainda precisa compor/injetar a implementação concreta; sem uma composição clara, pode continuar acoplada ao adapter.

## Evidências

- `4202941` adicionou o repositório do agregado `ItemEmprestado` e os testes associados.
- `68ead2f` registra o uso do padrão Repository para o agregado de Acervo.
- A CI executa testes unitários com fake e testes de integração com SQLite, confirmando a existência dos dois caminhos de teste.
