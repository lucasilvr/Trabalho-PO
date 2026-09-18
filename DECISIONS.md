# DECISIONS

## Sandy Fortes Cabral

### Fase 1 — Checkpoint 1

#### Implementação

Implementei o comportamento inicial do agregado Empréstimo, comecei pela entidade ItemEmprestado. A entidade representa um exemplar associado a um empréstimo e permite verificar se a devolução está em atraso.

#### Arquivos

- `src/biblioteca/domain/model.py`
- `tests/unit/test_emprestimo.py`

#### Testes

Foi implementado um teste unitário para verificar que um item é considerado atrasado quando a data de referência ultrapassa a data prevista de devolução e a devolução ainda não foi registrada.

#### Decisão de projeto

A verificação de atraso recebe uma data de referência como parâmetro, em vez de consultar diretamente a data atual do sistema,permitindo controlar as datas utilizadas nos testes.