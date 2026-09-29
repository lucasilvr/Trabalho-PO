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
- `tests/unit/test_emprestimo.py`

#### Testes

18 - 09 - 2026
Foi implementado um teste unitário para verificar que um item é considerado atrasado quando a data de referência ultrapassa a data prevista de devolução e a devolução ainda não foi registrada.

19 - 09 - 2026
Foi implementado um teste para verificar que, após o registro da devolução, a data é armazenada e o item deixa de ser considerado atrasado.

#### Decisão de projeto

18 - 09 - 2026
A verificação de atraso recebe uma data de referência como parâmetro, em vez de consultar diretamente a data atual do sistema, permitindo controlar as datas utilizadas nos testes.

19 - 09 - 2026
O registro da devolução foi modelado como comportamento da entidade `ItemEmprestado`, pois representa uma mudança de estado do próprio objeto de domínio.

### Fase 1 — Checkpoint 2

#### Implementação

21 - 09 - 2026
`a980f4e` — feat: implementa mapeamento ORM de ItemEmprestado
Implementei o mapeamento ORM da entidade ItemEmprestado utilizando SQLAlchemy, criando a tabela correspondente e configurando o mapeamento entre a entidade do domínio e a tabela do banco de dados.

23 - 09 - 2026
`4202941` — feat: implementa repository de ItemEmprestado
Implementei o repositório da entidade ItemEmprestado, criando o contrato AbstractRepository, a implementação real SqlAlchemyRepository e o FakeRepository para utilização nos testes.

#### Arquivos

- `src/biblioteca/adapters/__init__.py`
- `src/biblioteca/adapters/orm.py`
- `src/biblioteca/adapters/repository.py`
- `tests/integration/test_emprestimo_orm.py`
- `tests/integration/test_emprestimo_repository.py`
- `tests/unit/test_fake_repository.py`
- `requirements.txt`

#### Testes

21 - 09 - 2026
Foi implementado um teste de integração utilizando SQLite em memória para verificar que um registro armazenado na tabela de itens emprestados pode ser carregado novamente como um objeto ItemEmprestado.

23 - 09 - 2026
Foi implementado um teste unitário utilizando FakeRepository para verificar as operações de adição, busca e listagem de itens.

23 - 09 - 2026
Foi implementado um teste de integração utilizando SqlAlchemyRepository e SQLite em memória para verificar as operações de adição, busca e listagem de itens persistidos.

#### Decisão de projeto

21 - 09 - 2026
O mapeamento da entidade foi colocado no módulo de adapters, mantendo o domínio separado do SQLAlchemy e evitando que a entidade ItemEmprestado tenha dependência direta da infraestrutura de persistência.

23 - 09 - 2026
Foi utilizada uma abstração AbstractRepository para separar as operações de persistência da implementação do banco de dados, permitindo utilizar o FakeRepository nos testes e o SqlAlchemyRepository na persistência real.

### Fase 1 — Entrega

#### Implementação
28 - 09 - 2026
`719453d` — feat: implementa service layer e API de Emprestimo
Implementei a camada de serviço do módulo Empréstimo, criando operações para registrar empréstimo, registrar devolução e consultar atraso. Também implementei a API Flask correspondente aos casos de uso e os testes E2E dos endpoints.

#### Arquivos

- `src/biblioteca/service_layer/__init__.py`
- `src/biblioteca/service_layer/services.py`
- `src/biblioteca/entrypoints/__init__.py`
- `src/biblioteca/entrypoints/flask_app.py`
- `tests/unit/test_services_emprestimo.py`
- `tests/e2e/test_emprestimo_api.py`
- `requirements.txt`

#### Testes

28 - 09 - 2026
Foram implementados quatro testes unitários para verificar a camada de serviço utilizando FakeRepository, cobrindo o registro de empréstimo, o registro de devolução e a consulta de atraso.

28 - 09 - 2026
Foram implementados quatro testes E2E para verificar os endpoints da API de Empréstimo, cobrindo o registro de empréstimo, o registro de devolução, a consulta de atraso e o tratamento de item inexistente.

#### Decisão de projeto

28 - 09 - 2026
A camada de serviço foi utilizada para orquestrar as operações entre a API, o repositório e as entidades do domínio, mantendo as regras de negócio relacionadas ao ItemEmprestado na própria entidade.

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

### Fase 1 - Entrega

#### Implementação

29-09-2026 
`b6061d5` — chore: adicionar github actions workflow
Foi adicionado um workflow do GitHub Actions para automatizar a execução das validações do projeto a cada push e pull request. O pipeline realiza verificações de qualidade do código e execução dos testes, garantindo que alterações futuras não introduzam regressões e mantendo a consistência do processo de integração contínua.

`8659f0f` — test: adicionar conftest
Implementação do conftest.py para centralizar fixtures compartilhadas entre os testes, reduzindo duplicação de código, e facilitando a criação de cenários de teste reutilizáveis.

`b9366aa` — feat: implementar service_layer com ajustes na coesão
Desenvolvimento da camada de serviço (service_layer) para concentrar os casos de uso da aplicação e coordenar a interação entre domínio e repositórios. Durante a implementação, foram realizados ajustes para melhorar a coesão das responsabilidades, mantendo as regras de negócio dentro do domínio e delegando à camada de serviço apenas a orquestração das operações da aplicação.

`ca87c3a` — feat: implementar API flask
Foi desenvolvida uma API utilizando Flask para expor as funcionalidades da aplicação através de endpoints HTTP, permitindo a comunicação com as regras de negócio por meio da camada de serviço e estabelecendo a interface de entrada do sistema.

#### Arquivos

- `.github/workflows/ci.yml`
- `src/biblioteca/service_layer/services.py`
- `src/biblioteca/entrypoints/flask_app.py`
- `tests/e2e/test_services.py`
- `tests/e2e/test_api.py`
- `tests/conftest.py`
- `tests/pytest.ini`

#### Testes

29-09-2026 
`b9366aa` — feat: implementar service_layer com ajustes na coesão
Os testes da service_layer validam a interação entre a camada de aplicação e o repositório, garantindo que as operações de negócio sejam executadas correctamente através do uso do FakeRepository.

`c93e7dd` —  test: adicionar teste da API
Foram adicionados testes para validar o comportamento dos endpoints da API Flask. Os testes verificam as respostas retornadas pela aplicação, os códigos de status HTTP esperados e a integração entre a camada de apresentação e os casos de uso, garantindo o correto funcionamento da interface exposta ao cliente.

#### Decisão de projeto

Centralizar a criação de objetos de teste no conftest.py para promover reutilização e garantir a consistência na configuração dos testes em todas as camadas da aplicação.
