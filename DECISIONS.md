# DECISIONS

## Sandy Fortes Cabral

### Fase 1 — Checkpoint 1

#### Implementação

18 - 09 - 2026
Implementei o comportamento inicial do agregado Empréstimo, comecei pela entidade ItemEmprestado. A entidade representa um exemplar associado a um empréstimo e permite verificar se a devolução está em atraso.

19 - 09 - 2026
Implementei o registro da devolução, permitindo atualizar o estado do item quando ele é devolvido.

#### Arquivos

- `src/biblioteca/domain/model.py`
- `tests/unit/test_emprestimo.py`

#### Testes

18 - 09 - 2026
Foi implementado um teste unitário para verificar que um item é considerado atrasado quando a data de referência ultrapassa a data prevista de devolução e a devolução ainda não foi registrada.

19 - 09 - 2026
Foi implementado um teste para verificar que, após o registro da devolução, a data é armazenada e o item deixa de ser considerado atrasado.

#### Decisão de projeto

18 - 09 - 2026
A verificação de atraso recebe uma data de referência como parâmetro, em vez de consultar diretamente a data atual do sistema,permitindo controlar as datas utilizadas nos testes.

19 - 09 - 2026
O registro da devolução foi modelado como comportamento da entidade `ItemEmprestado`, pois representa uma mudança de estado do próprio objeto de domínio.