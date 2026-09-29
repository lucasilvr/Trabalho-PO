# DECISIONS

## Sandy Fortes Cabral

### Fase 1 — Checkpoint 1

#### Implementação
18-09-2026 
`3b28cea` — feat: implementa regra de atraso do item emprestado
Implementei o comportamento inicial do agregado Empréstimo, comecei pela entidade ItemEmprestado. A entidade representa um exemplar associado a um empréstimo e permite verificar se a devolução está em atraso.

19-09-2026 
`a3e880a` — feat: adiciona registro de devolucao ao item emprestado
Implementei o registro da devolução, permitindo atualizar o estado do item quando ele é devolvido.

#### Testes
18-09-2026 
Foi implementado um teste unitário para verificar que um item é considerado atrasado quando a data de referência ultrapassa a data prevista de devolução e a devolução ainda não foi registrada.

19-09-2026 
Foi implementado um teste para verificar que, após o registro da devolução, a data é armazenada e o item deixa de ser considerado atrasado.

#### Decisão de projeto
18-09-2026 
A verificação de atraso recebe uma data de referência como parâmetro, em vez de consultar diretamente a data atual do sistema, permitindo controlar as datas utilizadas nos testes.

19-09-2026 
O registro da devolução foi modelado como comportamento da entidade `ItemEmprestado`, pois representa uma mudança de estado do próprio objeto de domínio.

### Fase 1 — Checkpoint 2

#### Implementação
21-09-2026 
`a980f4e` — feat: implementa mapeamento ORM de ItemEmprestado
Implementei o mapeamento ORM da entidade ItemEmprestado utilizando SQLAlchemy, criando a tabela correspondente e configurando o mapeamento entre a entidade do domínio e a tabela do banco de dados.

23-09-2026 
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
21-09-2026 
Foi implementado um teste de integração utilizando SQLite em memória para verificar que um registro armazenado na tabela de itens emprestados pode ser carregado novamente como um objeto ItemEmprestado.

23-09-2026 
Foi implementado um teste unitário utilizando FakeRepository para verificar as operações de adição, busca e listagem de itens. Teste de integração com SqlAlchemyRepository também implementado para validar persistência.

#### Decisão de projeto
21-09-2026 
O mapeamento da entidade foi colocado no módulo de adapters, mantendo o domínio separado do SQLAlchemy e evitando que a entidade ItemEmprestado tenha dependência direta da infraestrutura de persistência.

23-09-2026 
Foi utilizada uma abstração AbstractRepository para separar as operações de persistência da implementação do banco de dados, permitindo utilizar o FakeRepository nos testes e o SqlAlchemyRepository na persistência real.

### Fase 1 — Entrega

#### Implementação
28-09-2026 
`719453d` — feat: implementa service layer e API de Emprestimo
Implementei a camada de serviço do módulo Empréstimo, criando operações para registrar empréstimo, registrar devolução e consultar atraso. Também implementei a API Flask correspondente aos casos de uso e os testes E2E dos endpoints.

#### Arquivos
- `src/biblioteca/service_layer/__init__.py`
- `src/biblioteca/service_layer/services.py`
- `src/biblioteca/entrypoints/__init__.py`
- `src/biblioteca/entrypoints/flask_app.py`
- `tests/unit/test_services_emprestimo.py`
- `tests/e2e/test_emprestimo_api.py`

#### Testes
28-09-2026 
Implementados quatro testes unitários na camada de serviço com FakeRepository e quatro testes E2E para verificar os endpoints da API de Empréstimo.

#### Decisão de projeto
28-09-2026 
A camada de serviço foi utilizada para orquestrar as operações entre a API, o repositório e as entidades do domínio, mantendo as regras de negócio relacionadas ao ItemEmprestado na própria entidade.

---

## Karine Vitória Marinho de Moraes

### Fase 1 - Checkpoint 1

#### Implementação
23-09-2026 
`505aceb` — feat: criar entidades
Realizei a implementação do agregado, sendo composto pelas entidades "OrdemServico", "LaudoAvaliacao", e "OrdemServicoStatus".

28-09-2026 
`a66c65` — feat: implementar comportamento nas entidades
Foquei na validação das condições necessárias para a criação e execução da reparação de dano no exemplar.

#### Arquivos
- `src/biblioteca/domain/model.py`
- `tests/unit/test_manutencao.py`

#### Testes
28-09-2026 
`2200aac` — feat: adicionar testes unitários
Testes unitários verificam as regras de criação do agregado, validando a criação de OrdemServico com status "ABERTA" e a regra que impede a criação quando o dano não é reparável.

#### Decisão de projeto
A utilização do Enum teve como objetivo representar possíveis status da OrdemServico com valores padronizados.

### Fase 1 - Checkpoint 2

#### Implementação
28-09-2026 
`5f1166b` — feat: implementar estrutura do orm
Realizei a implementação do ORM com o SQLAlchemy, mapeando as entidades existentes e relacionando OrdemServico e LaudoAvaliacao.

29-09-2026 
`6820456` — feat: implementar repository e teste de integracao
Desenvolvimento do repository com operações de adicionar, buscar e listar as OrdemServico.

#### Arquivos
- `src/biblioteca/adapters/orm.py`
- `src/biblioteca/adapters/repository.py`
- `tests/integration/test_repository.py`

#### Testes
29-09-2026 
Testes de integração utilizando banco SQLite em memória para validar criação, busca por ID e listagem geral de OrdemServico. Ajustes feitos no commit `6961be2` para corrigir pequenas quebras lógicas.

#### Decisão de projeto
A decisão de manter as entidades LaudoAvaliacao e OrdemServico em tabelas separadas foi tomada para representar melhor a estrutura do domínio.

### Fase 1 - Entrega

#### Implementação
29-09-2026 
`b6061d5` — chore: adicionar github actions workflow
Adicionado workflow do GitHub Actions para automatizar validações. Implementado `conftest.py` (`8659f0f`), a `service_layer` (`b9366aa`) e a API Flask (`ca87c3a`).

#### Arquivos
- `.github/workflows/ci.yml`
- `src/biblioteca/service_layer/services.py`
- `src/biblioteca/entrypoints/flask_app.py`
- `tests/e2e/test_services.py`
- `tests/e2e/test_api.py`
- `tests/conftest.py`

#### Testes
29-09-2026 
Testes da service_layer validam a interação com FakeRepository. Testes da API verificam as respostas HTTP e integração entre apresentação e casos de uso.

#### Decisão de projeto
Centralizar a criação de objetos de teste no conftest.py para promover reutilização e garantir a consistência na configuração dos testes.

---

## Lucas Dias Silveira

### Fase 1 — Checkpoint 1

#### Implementação
Implementei o modelo de domínio do agregado de Acervo. Criei as entidades `Livro` (Raiz de Agregado) e `Exemplar`, além de implementar a regra de negócio central que impede a inativação de um livro no catálogo caso ele possua exemplares com status de "emprestado".

#### Arquivos
- `src/biblioteca/acervo/domain/model.py`
- `tests/unit/test_acervo.py`

#### Testes
Foram desenvolvidos testes unitários puros cobrindo o modelo de domínio, validando a adição correta de exemplares a um livro e garantindo que a exceção de inativação seja disparada corretamente em caso de violação de regra de negócio.

#### Decisão de projeto
Escolhi modelar `Livro` como a Raiz de Agregado pois o ciclo de vida do `Exemplar` depende da existência prévia de um catálogo. A regra de negócio principal (inativação) foi mantida isolada, garantindo que o domínio não tenha dependências externas (Python puro).

### Fase 1 — Checkpoint 2

#### Implementação
Implementa padrão repository para o acervo.
Desenvolvi o mapeamento ORM e o Padrão Repository para o agregado de Acervo. Implementei o contrato `AbstractRepository`, o banco real com `SqlAlchemyRepository` e o banco em memória para testes com `FakeRepository`. 

#### Arquivos
- `src/biblioteca/acervo/adapters/orm.py`
- `src/biblioteca/acervo/adapters/repository.py`
- `tests/integration/test_repository.py`

#### Testes
Implementado teste de integração utilizando SQLite em memória e execução de queries SQL puras para comprovar que o `SqlAlchemyRepository` está persistindo e resgatando as entidades de `Livro` e `Exemplar` de forma consistente.

#### Decisão de projeto
Optei pela abordagem de Mapeamento Imperativo (Clássico) do SQLAlchemy no arquivo `orm.py`. Isso permitiu que a entidade de domínio continuasse "limpa" e livre de heranças do framework de banco de dados, aplicando corretamente o Princípio da Inversão de Dependência (DIP).

### Fase 1 — Entrega

#### Implementação
Orquestra casos de uso e cria rotas web HTTP
Criei a camada de serviços orquestrando a injeção de dependências para as funções de adicionar e inativar livros. Em seguida, implementei os Entrypoints com Flask, disponibilizando as rotas POST para consumo da API.

#### Arquivos
- `src/biblioteca/acervo/service_layer/services.py`
- `src/biblioteca/entrypoints/flask_app.py`
- `tests/e2e/test_api.py`

#### Testes
Foram criados testes End-to-End simulando um cliente real com a biblioteca `requests`, validando o fluxo completo: requisição HTTP na rota do Flask, orquestração na camada de serviço, passagem pelo modelo de domínio e salvamento físico no banco SQLite.

#### Decisão de projeto
O uso de injeção de dependências no `services.py` permitiu desacoplar completamente o framework web (Flask) das regras do banco de dados e do domínio. O arquivo `.db` foi adicionado ao `.gitignore` para garantir que o banco de persistência local não interfira no repositório compartilhado do grupo.

---

## João Vicente Piller Menezes

### Fase 1 — Checkpoint 1

#### Implementação
22-09-2026 
`f185330` — feat: implementa entidade Reserva e limite de 48 horas
Implementei o agregado Reserva e estabeleci as lógicas iniciais de verificação de prazo.

23-09-2026 
`99b7408` — feat: implementa agregado FilaEspera com transferencia de direito
Implementei a entidade raiz FilaEspera, encarregada de gerenciar a fila e garantir a transferência de exemplares devolvidos para o próximo da fila, respeitando a invariante de 48 horas estipulada na proposta.

#### Arquivos
- `src/biblioteca/reservas/domain/model.py`
- `src/biblioteca/reservas/tests/unit/test_reserva.py`
- `src/biblioteca/reservas/tests/unit/test_fila_espera.py`

#### Testes
22-09-2026 
Testes unitários cobrindo transições de estados de uma reserva (Pendente, Disponível e Expirada).

23-09-2026 
Teste unitário protegendo a invariante principal do domínio em `atualizar_fila()`.

#### Decisão de projeto
22-09-2026 
A verificação `esta_expirada` recebe `data_hora_atual` como injeção de dependência via parâmetro de método, viabilizando o mock da passagem do tempo durante a bateria de testes unitários.

### Fase 1 — Checkpoint 2

#### Implementação
28-09-2026 
`2496e8f` — feat: adiciona mapeamento ORM para reserva e fila de espera

29-09-2026 
`75a7802` — feat: adiciona repository pattern e integra ORM no Checkpoint 2
Abstração do acesso a banco via Repository, conforme o livro-texto, mantendo total ausência de dependências de infraestrutura na modelagem inicial.

#### Arquivos
- `src/biblioteca/reservas/adapters/orm.py`
- `src/biblioteca/reservas/adapters/repository.py`
- `src/biblioteca/reservas/tests/integration/test_reserva_orm.py`

#### Testes
29-09-2026 
Implementação do teste de integração com SQLite instanciado em memória, garantindo persistência em cascata da lista de reservas aninhadas a uma fila.

#### Decisão de projeto
29-09-2026 
Optei por não criar um repositório isolado para a `Reserva`. Sendo ela um objeto interno do agregado, suas persistências deverão ser lidadas exclusivamente através da entidade raiz `FilaEspera`, preservando a consistência arquitetural.

### Fase 1 — Entrega

#### Implementação
29-09-2026 
Reorganizei o módulo de Reservas na estrutura adotada pelo grupo (`src/biblioteca/reservas/` com `domain`, `adapters`, `service_layer`, `entrypoints` e `tests`). Implementei a camada de serviço com os casos de uso de reservar livro, registrar devolução de exemplar, atualizar a fila (expiração de 48 horas) e consultar a fila, além da API Flask correspondente. Também adicionei o `FakeFilaEsperaRepository` e o método `list` ao repositório.

#### Arquivos
- `src/biblioteca/reservas/adapters/repository.py`
- `src/biblioteca/reservas/service_layer/services.py`
- `src/biblioteca/reservas/entrypoints/flask_app.py`
- `src/biblioteca/reservas/tests/unit/test_fake_repository_reservas.py`
- `src/biblioteca/reservas/tests/unit/test_services_reservas.py`
- `src/biblioteca/reservas/tests/integration/test_reserva_repository.py`
- `src/biblioteca/reservas/tests/e2e/test_reservas_api.py`

#### Testes
29-09-2026 
Testes unitários da camada de serviço com `FakeFilaEsperaRepository`, testes de integração com SQLite em memória validando a recuperação da fila na ordem de chegada e a persistência das mudanças de status, e testes E2E cobrindo os endpoints `POST /reservas`, `POST /filas/<id_livro>/devolucao`, `POST /filas/<id_livro>/atualizacao` e `GET /filas/<id_livro>`.

#### Decisão de projeto
29-09-2026 
Os endpoints de devolução e atualização operam sobre a `FilaEspera`, e não sobre a `Reserva` isolada, pois a invariante de transferência do direito após 48 horas pertence à raiz do agregado. O relacionamento ORM ordena as reservas por `data_reserva`, garantindo que a ordem de chegada da fila seja preservada ao carregar do banco. A data e hora de referência continuam sendo recebidas como parâmetro, mantendo os casos de uso testáveis sem depender do relógio do sistema.
# DECISIONS

## Ana Laura

### Fase 1 — Checkpoint 1

#### Implementação

23 - 09 - 2026 e 25 - 09 - 2026
`2d34527` — chore: inicializa pacote de dominio
`1956c77` — chore: inicializa pacote de adaptadores
`362f17e` — chore: arquivo de registros de decisoes individuais criado
`abdc50e` — chore: arquivo init.py da biblioteca criado
`d0b2356` — chore: arquivos de requirements criado
Criei a estrutura de pastas do meu agregado e o arquivo de decisões individuais. Também adicionei as dependências iniciais do projeto.

28 - 09 - 2026
`d64eec2` — feat: entidades multa e pagamento criadas
Desenvolvi a raiz de agregado `Multa` e o value object `Pagamento`. A classe principal agora protege a invariante, alterando o status apenas com o pagamento total.

#### Arquivos

- `src/biblioteca/domain/model.py`
- `tests/unit/test_multas.py`
- `requirements.txt`
- `DECISIONS.md`

#### Testes

28 - 09 - 2026 Criei testes unitários para garantir que a regra de quitação da multa funciona. Eles validam tanto pagamentos exatos quanto pagamentos insuficientes.

#### Decisão de projeto

28 - 09 - 2026 Modelei `Pagamento` como Value Object por ser apenas um registro transacional imutável. Mantive a checagem de quitação dentro de `Multa` para não vazar a regra de negócio.

### Fase 1 — Checkpoint 2

#### Implementação

28 - 09 - 2026
`2392022` — feat: interface de repositorio fake para as multas criado
`2dd4b59` — fix: correção na busca no repository.py
Criei as interfaces do repositório de multas e a versão Fake em memória. Troquei o ID na busca aqui, gerando um bug que só encontrei depois.

29 - 09 - 2026
`39f04f5` — feat: mapeamento orm de multa e pagamento criados
Fiz o mapeamento das entidades para o banco de dados usando SQLAlchemy. Configurei as tabelas de multas e pagamentos de forma imperativa.

#### Arquivos

- `src/biblioteca/adapters/__init__.py`
- `src/biblioteca/adapters/orm.py`
- `src/biblioteca/adapters/repository.py`

#### Testes

(Os testes de integração do ORM foram consolidados junto à criação do repositório fake e do mapeamento).

#### Decisão de projeto

29 - 09 - 2026 Isolei o mapeamento no adapter usando o SQLAlchemy de forma imperativa. Isso manteve meu domínio puro e sem dependências diretas da infraestrutura.

### Fase 1 — Entrega

#### Implementação

29 - 09 - 2026 `2e276da` — fix: correção da funca de busca no repositorio fake (multa)
Consertei o `FakeMultaRepository`, que buscava a multa pelo `id_leitor` em vez de `id_multa`. O erro estourou enquanto eu implementava os testes da camada de serviço.

29 - 09 - 2026
`433bcd6` — feat: service layer criada
`b9de837` — feat: api de processamento de pagamento criada
Construí o service para orquestrar a baixa da multa e criei o endpoint POST no Flask. Agora a API recebe a requisição e salva as alterações no repositório.

#### Arquivos

- `src/biblioteca/service_layer/services.py`
- `src/biblioteca/entrypoints/flask_app.py`
- `tests/unit/test_services.py`

#### Testes

29 - 09 - 2026 Fiz o teste unitário do service, que me salvou e ajudou a achar o erro do repositório fake. Depois da correção, o fluxo passou a rodar perfeitamente.

#### Decisão de projeto

29 - 09 - 2026 Deixei o service apenas orquestrando chamadas entre API e repositório. Toda a regra de validação do valor continuou presa com segurança na entidade `Multa`.