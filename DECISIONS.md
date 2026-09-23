# DECISIONS

## Sandy Fortes Cabral

### Fase 1 — Checkpoint 1

#### Implementação

18 - 09 - 2026
`3b28cea` — feat: implementa regra de atraso do item emprestado
Implementei o comportamento inicial do agregado Empréstimo, comecei pela entidade ItemEmprestado. A entidade representa um exemplar associado a um empréstimo e permite verificar se a devolução está em atraso.

19 - 09 - 2026
`a3e880a` — feat: adiciona registro de devolucao ao item emprestado
Implementei o registro da devolução, permitindo atualizar o estado do item quando ele é devolvido.

**#### Implementação**

21 - 09 - 2026

`a980f4e` — feat: implementa mapeamento ORM de ItemEmprestado
Implementei o mapeamento ORM da entidade ItemEmprestado utilizando SQLAlchemy, criando a tabela correspondente e configurando o mapeamento entre a entidade do domínio e a tabela do banco de dados.

23 - 09 - 2026

Implementei o repositório da entidade ItemEmprestado, criando o contrato AbstractRepository, a implementação real SqlAlchemyRepository e o FakeRepository para utilização nos testes.

#### Arquivos

- `src/biblioteca/domain/model.py`
- `tests/unit/test_emprestimo.py`
- `src/biblioteca/adapters/repository.py`
- `tests/unit/test_emprestimo_repository.py`
- `tests/integration/test_emprestimo_repository.py`

#### Testes

18 - 09 - 2026
Foi implementado um teste unitário para verificar que um item é considerado atrasado quando a data de referência ultrapassa a data prevista de devolução e a devolução ainda não foi registrada.

19 - 09 - 2026
Foi implementado um teste para verificar que, após o registro da devolução, a data é armazenada e o item deixa de ser considerado atrasado.

23 - 09 - 2026

Foi implementado um teste unitário utilizando FakeRepository para verificar as operações de adição, busca e listagem de itens. E também um teste de integração utilizando SqlAlchemyRepository e SQLite em memória para verificar as operações de adição, busca e listagem de itens persistidos.

#### Decisão de projeto

18 - 09 - 2026
A verificação de atraso recebe uma data de referência como parâmetro, em vez de consultar diretamente a data atual do sistema,permitindo controlar as datas utilizadas nos testes.

19 - 09 - 2026
O registro da devolução foi modelado como comportamento da entidade `ItemEmprestado`, pois representa uma mudança de estado do próprio objeto de domínio.

23 - 09 - 2026

Foi utilizada uma abstração AbstractRepository para separar as operações de persistência da implementação do banco de dados, permitindo utilizar o FakeRepository nos testes e o SqlAlchemyRepository na persistência real.

### Fase 1 — Checkpoint 2

#### Implementação

21 - 09 - 2026

Implementei o mapeamento ORM da entidade ItemEmprestado utilizando SQLAlchemy, criando a tabela correspondente e configurando o mapeamento entre a entidade do domínio e a tabela do banco de dados.

#### Arquivos

- `src/biblioteca/adapters/orm.py`

- `tests/integration/test_emprestimo_orm.py`

#### Testes

21 - 09 - 2026

Foi implementado um teste de integração utilizando SQLite em memória para verificar que um registro armazenado na tabela de itens emprestados pode ser carregado novamente como um objeto ItemEmprestado.

#### Decisão de projeto

21 - 09 - 2026

O mapeamento da entidade foi colocado no módulo de adapters, mantendo o domínio separado do SQLAlchemy e evitando que a entidade ItemEmprestado tenha dependência direta da infraestrutura de persistência.
