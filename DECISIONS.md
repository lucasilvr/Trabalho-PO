# DECISIONS

## Karine Vitória Marinho de Moraes

### Fase 1 - Checkpoint 1

#### Implementação

23-09-2026 
`505aceb` — feat: criar entidades
Realizei a implementação do agregado, sendo composto pelas entidades "OrdemServico", que representa a solicitação de manutenção, e "LaudoAvaliacao", que registra as infromações relacionadas ao dano no exemplar, além do "OrdemServicoStatus", responsável por padronizar os estados possíveis de uma ordem de serviço.

28-09-2026 
`a66c65` — feat: implementar comportamento nas entidades
Foquei na validação das condições necessárias para a criação e execução da reparação de dano no exemplar.

#### Arquivos

- `src/biblioteca/domain/model.py`

- `tests/unit/test_manutencao.py`

#### Testes

28-09-2026 
`2200aac` — feat: adicionar testes unitários
Os testes unitários verificam as principais regras de criação do agregado: 
- O primeiro teste valida a criação de uma OrdemServico com dados válidos com o status "ABERTA".
- O segundo teste verifica a regra de negócio que impede a criação de uma OrdemServico quando o dano não é reparável.

#### Decisão de projeto

A utilização do Enum teve como objetivo representar possíveis status da OrdemServico com valores padronizados.


### Fase 1 - Checkpoint 2

#### Implementação

28-09-2026 
`5f1166b` — feat: implementar estrutura do orm
Realizei a implementação do ORM com o SQLAlchemy, mapeando as entidades existentes no agregado para tabelas, relacionando OrdemServico e LaudoAvaliacao a partir de uma chave estrangeira.

29-09-2026
`6820456` — feat: implementar repository e teste de integracao
O repository foi desenvolvido com operações de adicionar, buscar e listar as OrdemServico, abstraindo o acesso aos dados por meio do ORM anteriormente implementado.

#### Arquivos

- `src/biblioteca/adapters/orm.py`

- `src/biblioteca/adapters/repository.py`

- `tests/integration/test_repository.py`

#### Testes

29-09-2026 
`6820456` — feat: implementar repository e teste de integracao
Os testes de integração utilizam um banco de dados SQLite em memória para verificar o funcionamento do repository: 
- O primeiro teste valida a criação de uma OrdemServico dentro do banco de dados e sua posterior busca pelo seu ID, verificando também o relacionamento da OrdemServico com o LaudoAvaliacao.
- O segundo teste verifica se a implementação garante a listagem de todas as OrdemServico cadastradas, garantindo a quantidade de registros e seus respectivos IDs.

`6961be2` — fix: ajustar erros encontrados nos testes
Após a implementação dos testes unitário e integrado, eu rodei os testes para descobrir eventuais inconsistências no código. Solucionei pequenas quebras de lógica para que o sistema funcionasse conforme esperado.

#### Decisão de projeto

A decisão de manter as entidades LaudoAvaliacao e OrdemServico em tabelas separadas foi tomada para representar melhor a estrutura do domínio e manter a separação das informações.