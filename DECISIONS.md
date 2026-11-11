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

### Fase 2 — Checkpoint 1

#### Implementação

22 - 10 - 2026

Contribuí para a documentação da arquitetura do sistema Biblioteca, descrevendo os estilos arquiteturais existentes, os atributos de qualidade priorizados, os trade-offs e a comparação com uma arquitetura alternativa. Também documentei a decisão de separar o domínio da infraestrutura de persistência por meio de um ADR relacionado ao módulo Empréstimo.

#### Arquivos

- `docs/arquitetura.md`
- `docs/adr/0001-separacao-dominio-persistencia.md`

#### Testes

22 - 10 - 2026

Conferi a documentação em relação à estrutura do código existente e aos componentes de domínio, persistência, camada de serviço e API. A validação da suíte automatizada deve ser confirmada pela CI do repositório.

#### Decisão de projeto

22 - 10 - 2026

Registrei a separação entre domínio e persistência como uma decisão arquitetural, considerando o benefício de testar as regras de negócio sem depender diretamente do SQLAlchemy e o custo de manter camadas e abstrações adicionais.

#### Uso de IA

Utilizei IA generativa para auxiliar na elaboração e organização de um rascunho da documentação de arquitetura e do ADR. Revisei o conteúdo em relação ao código e ao histórico do repositório, sendo responsável pelas verificações, ajustes e versão final.

### Fase 2 — Checkpoint 2

#### Implementação

`f275b6f` — refactor(emprestimo): unifica contrato de item não encontrado

Refatorei o contrato do repositório do agregado Empréstimo. Antes, `SqlAlchemyRepository.get` lançava `NoResultFound` e `FakeRepository.get` lançava `StopIteration` para o mesmo caso de item inexistente. Criei `ItemNaoEncontrado` no domínio, passei as duas implementações a levantar essa exceção e removi do entrypoint Flask o import de `NoResultFound`. No mesmo commit, documentei a violação, o código anterior, a refatoração e o custo em `docs/solid.md`.

#### Arquivos

- `src/biblioteca/emprestimo/domain/exceptions.py`
- `src/biblioteca/emprestimo/adapters/repository.py`
- `src/biblioteca/emprestimo/entrypoints/flask_app.py`
- `src/biblioteca/emprestimo/tests/unit/test_repository_contract.py`
- `src/biblioteca/emprestimo/tests/integration/test_emprestimo_repository.py`
- `src/biblioteca/emprestimo/tests/e2e/test_emprestimo_api.py`
- `docs/solid.md`

#### Testes

02/11/2026

Mantive os testes da Fase 1 sem alteração e acrescentei testes para o contrato do repositório: o fake e o repositório SQLAlchemy devem levantar `ItemNaoEncontrado` para um item ausente. Também acrescentei um teste E2E para o endpoint de atraso com item inexistente. A suíte do Empréstimo passou com `25 passed`.

#### Decisão de projeto

02/11/2026

Padronizei a ausência de item como uma exceção de domínio (`ItemNaoEncontrado`) em vez de deixar cada adapter expor a exceção nativa da sua tecnologia, porque o contrato do repositório precisa ser substituível sem alterar a camada HTTP.

#### Uso de IA

Utilizei IA generativa para analisar o código em busca de violações de SOLID, comparar alternativas de refatoração e organizar o rascunho de `docs/solid.md` e desta subseção. Conferi os trechos citados nos commits `4202941`, `719453d` e `1cd3fa3`, executei a suíte de testes e revisei o texto final; a decisão e a responsabilidade pela alteração são minhas.

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

### Fase 2 — Checkpoint 1

#### Implementação

Documentei uma decisão arquitetural relacionada ao módulo de Penalidades, considerando a separação entre a API, a camada de serviço e as operações do domínio. O ADR apresenta o contexto da decisão, as alternativas consideradas e suas consequências para a organização e manutenção do módulo.

#### Arquivos

- docs/adr/0003-api-flask-multas.md

#### Testes

Conferi a decisão documentada em relação à implementação existente do módulo de Penalidades e às verificações automatizadas do projeto.

#### Decisão de projeto


A decisão documentada busca manter as responsabilidades da interface HTTP separadas da orquestração dos casos de uso e das regras de negócio do módulo de Penalidades.

#### Uso de IA

Se eu utilizar o rascunho produzido com auxílio de IA generativa, declararei esse uso e revisarei o conteúdo em relação ao código real de Penalidades, assumindo a responsabilidade pela versão final.

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
Reorganizei o módulo de Reservas na estrutura adotada pelo grupo (`src/biblioteca/reservas/` com `domain`, `adapters`, `service_layer`, `entrypoints` e `tests`). Defini a igualdade de `Reserva` e `FilaEspera` pela identidade (`id_reserva` e `id_livro`), adicionei o método `list` e o `FakeFilaEsperaRepository` ao repositório, e implementei a camada de serviço com os casos de uso de reservar livro, registrar devolução e atualizar a fila. Por fim, criei a API Flask que expõe esses casos de uso.

#### Arquivos
- `src/biblioteca/reservas/domain/model.py`
- `src/biblioteca/reservas/adapters/repository.py`
- `src/biblioteca/reservas/service_layer/services.py`
- `src/biblioteca/reservas/entrypoints/flask_app.py`
- `src/biblioteca/reservas/tests/unit/test_fake_repository_reservas.py`
- `src/biblioteca/reservas/tests/unit/test_services_reservas.py`
- `src/biblioteca/reservas/tests/integration/test_reserva_repository.py`
- `src/biblioteca/reservas/tests/e2e/test_reservas_api.py`

#### Testes
29-09-2026 
Testes unitários da camada de serviço usando `FakeFilaEsperaRepository` e uma `FakeSession`, que registra se o `commit` foi chamado. Testes de integração que inserem dados com SQL puro e verificam se o repositório recupera a fila com as reservas na ordem de chegada e lista todas as filas. Na API, um teste E2E do caminho feliz (reserva, devolução e transferência do direito após 48 horas) e um do caminho de erro (livro sem fila de espera).

#### Decisão de projeto
29-09-2026 
Os serviços recebem o repositório abstrato e a sessão, e fazem o commit somente no caminho feliz, deixando o endpoint Flask responsável apenas por traduzir a requisição HTTP e as exceções. A devolução e a atualização operam sobre a FilaEspera, e não sobre a Reserva isolada, pois a invariante de transferência do direito após 48 horas pertence à raiz do agregado. O relacionamento ORM ordena as reservas por data_reserva, preservando a ordem de chegada da fila ao carregar do banco.

### Fase 2 — Checkpoint 2

#### Implementação

02 - 11 - 2026
`14d6d57` — refactor(reservas): torna prazo de retirada configuravel (OCP)

Identifiquei uma violação do Princípio Aberto/Fechado (OCP) na entidade `Reserva`: o prazo de 48 horas para retirada estava fixo dentro de `esta_expirada` desde o commit `f185330` (22/09/2026). Diante de um requisito plausível, prazos diferentes por categoria de leitor (por exemplo, 72 horas para professores), a classe precisaria ser modificada a cada novo prazo. Transformei o prazo no atributo `prazo_retirada_horas`, com padrão de 48 horas, persistido em uma nova coluna da tabela `reservas` e aceito como parâmetro opcional no serviço `reservar_livro` e no endpoint `POST /reservas`.

03 - 11 - 2026
docs(reservas): documenta refatoracao OCP no solid.md (commit que acompanha esta subseção)

Documentei a violação, a refatoração, os testes e o custo em `docs/solid.md`, citando o commit "antes" (`f185330`) e o commit "depois" (`14d6d57`).

#### Arquivos

- `src/biblioteca/reservas/domain/model.py`
- `src/biblioteca/reservas/adapters/orm.py`
- `src/biblioteca/reservas/service_layer/services.py`
- `src/biblioteca/reservas/entrypoints/flask_app.py`
- `src/biblioteca/reservas/tests/unit/test_reserva.py`
- `src/biblioteca/reservas/tests/unit/test_services_reservas.py`
- `src/biblioteca/reservas/tests/integration/test_reserva_repository.py`
- `docs/solid.md`

#### Testes

02 - 11 - 2026

Os 16 testes existentes do módulo continuaram passando sem alteração, o que comprova que o comportamento padrão de 48 horas foi preservado. Adicionei 5 testes para o novo requisito: prazo padrão, reserva de 72 horas que não expira com 49 horas e expira com 73 horas, serviço com prazo personalizado, persistência do prazo no banco e leitura de uma reserva antiga sem prazo, que recebe o padrão de 48 horas.

#### Decisão de projeto

02 - 11 - 2026

Optei por tornar o prazo um atributo com valor padrão, em vez de criar uma hierarquia de classes de reserva, porque a regra de expiração é a mesma e apenas o valor muda. A coluna no banco recebe o mesmo valor padrão para que as reservas já gravadas continuem válidas sem migração de dados.

#### Uso de IA

Utilizei o Claude (Claude Code) para analisar o código do agregado e sugerir a violação de OCP, implementar a refatoração, escrever os novos testes e redigir um rascunho de `docs/solid.md` e desta subseção. Revisei o diff, rodei a suíte de testes antes de commitar e ajustei o texto, sendo responsável pelo resultado final.

### Fase 2 — Checkpoint 3

#### Implementação

06 - 11 - 2026
`014bb5c` — feat(reservas): adiciona estados da reserva para o padrao State

Criei as classes do padrão State no domínio de reservas: a interface `EstadoReserva`, que por padrão recusa todas as transições com `TransicaoInvalida`, e os estados concretos `ReservaPendente`, `ReservaDisponivel` e `ReservaExpirada`, além do dicionário `ESTADOS_RESERVA`, que liga o `status` persistido ao objeto de estado.

08 - 11 - 2026
`00a795e` — feat(reservas): aplica padrao State no ciclo de vida da Reserva

Fiz a `Reserva` delegar `disponibilizar`, `expirar` e `esta_expirada` ao estado atual, eliminando as condicionais com strings. Com isso, transições que antes passavam em silêncio passaram a ser recusadas: uma reserva expirada não volta a ficar disponível, uma reserva disponível não tem o prazo reiniciado e uma reserva pendente não expira sem ter ficado disponível.

09 - 11 - 2026
`5dae3d8` — docs(reservas): documenta padrao State no gof.md

Documentei o padrão em `docs/gof.md`, com o problema, as alternativas consideradas, os participantes, o diagrama de classes em Mermaid, os testes e o custo.

#### Arquivos

- `src/biblioteca/reservas/domain/model.py`
- `src/biblioteca/reservas/tests/unit/test_estado_reserva.py`
- `src/biblioteca/reservas/tests/unit/test_reserva.py`
- `docs/gof.md`

#### Testes

06 - 11 - 2026

Seis testes unitários em `test_estado_reserva.py` exercitam cada estado isoladamente, incluindo a correspondência entre os nomes dos estados e os valores de `status` gravados no banco.

08 - 11 - 2026

Quatro testes em `test_reserva.py` verificam as transições pela `Reserva`. Rodei esses quatro testes contra o código anterior ao padrão e todos falharam, confirmando que os problemas existiam. Os testes que já existiam no módulo continuaram passando sem alteração.

#### Decisão de projeto

08 - 11 - 2026

Mantive o `status` como texto na tabela `reservas` e fiz a `Reserva` encontrar o estado pelo dicionário `ESTADOS_RESERVA`, em vez de mapear os objetos de estado no ORM. Assim o banco e o mapeamento não mudaram, e uma reserva carregada do banco volta automaticamente ao estado correto.

#### Uso de IA

Utilizei o Claude (Claude Code) para escrever os testes e redigir os rascunhos de `docs/gof.md` (incluindo o diagrama Mermaid) e desta subseção. Revisei o código e os textos, rodei a suíte de testes antes de cada commit e sou responsável pelo resultado final.

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

- `src/biblioteca/multas/domain/model.py`
- `src/biblioteca/multas/tests/unit/test_multas.py`
- `requirements.txt`
- `DECISIONS.md`

#### Testes

28 - 09 - 2026 Criei testes unitários para garantir que a regra de quitação da multa funciona. Eles validam tanto pagamentos exatos quanto pagamentos insuficientes.

#### Decisão de projeto

28 - 09 - 2026 Modelei `Pagamento` como Value Object por ser apenas um registro transacional. Inicialmente utilizou-se imutabilidade estrita (`frozen=True`), que posteriormente precisou ser flexibilizada para garantir a integração com a injeção de estado do SQLAlchemy. Mantive a checagem de quitação dentro de `Multa` para não vazar a regra de negócio para a camada de serviços.

---

### Fase 1 — Checkpoint 2

#### Implementação

28 - 09 - 2026
`2392022` — feat: interface de repositorio fake para as multas criado
`2dd4b59` — fix: correção na busca no repository.py
Criei as interfaces do repositório de multas e a versão Fake em memória.

29 - 09 - 2026
`39f04f5` — feat: mapeamento orm de multa e pagamento criados
`3b9ac2f` — feat: classe do banco adicionada e caminho de importação corrigido
Fiz o mapeamento das entidades para o banco de dados usando SQLAlchemy de forma imperativa e adicionei a classe concreta do repositório (`SqlAlchemyMultaRepository`) para lidar com as operações reais.

#### Arquivos

- `src/biblioteca/multas/adapters/__init__.py`
- `src/biblioteca/multas/adapters/orm.py`
- `src/biblioteca/multas/adapters/repository.py`

#### Testes

29 - 09 - 2026 
`9567858` — test: correção dos tests e adicao do arquivo conftest.py
Criei os testes de integração para o repositório SQL (`test_multas_repository.py`), validando a persistência física dos agregados.

#### Decisão de projeto

29 - 09 - 2026 Isolei o mapeamento no adapter usando o SQLAlchemy de forma imperativa. Isso manteve meu domínio puro. A equipe decidiu manter a segregação arquitetural dentro das pastas de cada agregado (ex: `src/biblioteca/multas/domain`), pelo que todos os caminhos de importação foram ajustados para refletir este encapsulamento modular.

---

### Fase 1 — Entrega

#### Implementação

29 - 09 - 2026 
`2e276da` — fix: correção da busca no repositorio fake (multa)
`433bcd6` — feat: service layer criada
`b9de837` — feat: api de processamento de pagamento criada
`ec8daec` — chore: adicao do pacote requests
`ff9e5ba` — fix: importacoes ajustadas e arquivos __init__ faltantes adicionados
Consertei o `FakeMultaRepository`, construí o service para orquestrar a baixa da multa e criei o endpoint POST no Flask. Retifiquei todas as importações relativas ao pacote `multas` e instalei dependências em falta que estavam quebrando a pipeline de CI.

#### Arquivos

- `src/biblioteca/multas/service_layer/services.py`
- `src/biblioteca/multas/entrypoints/flask_app.py`
- `src/biblioteca/multas/tests/unit/test_services.py`
- `src/biblioteca/multas/tests/conftest.py`
- `src/biblioteca/multas/tests/e2e/test_api_multas.py`
- `src/biblioteca/multas/tests/integration/test_multas_repository.py`

#### Testes

29 - 09 - 2026 Adicionei o teste E2E real com chamadas de rede para simular o pagamento e um arquivo `conftest.py` local no módulo de multas para injetar um banco de dados SQLite em memória estritamente para o meu contexto, resolvendo conflitos de estado com outras partes do projeto.

#### Decisão de projeto

29 - 09 - 2026 Deixei o service apenas orquestrando chamadas entre API e repositório. Toda a regra de validação do valor continuou presa com segurança na entidade `Multa`.

---

### Fase 2 — Checkpoint 1

#### Implementação

22 - 10 - 2026

Documentei uma decisão arquitetural relacionada ao módulo Acervo, considerando a representação de livros e exemplares e a separação entre domínio e persistência. O ADR registra o contexto da decisão, as alternativas consideradas e suas consequências para a manutenção e evolução do módulo.

#### Arquivos

- `docs/adr/0002-modelagem-livro-exemplar.md`

#### Testes

22 - 10 - 2026

Conferi a decisão documentada em relação à implementação existente do Acervo e às verificações automatizadas do projeto.

#### Decisão de projeto

22 - 10 - 2026

A decisão documentada considera como a organização das entidades Livro e Exemplar representa o domínio e como a separação das responsabilidades afeta a manutenção e a evolução do Acervo.

---

### Fase 2 — Checkpoint 2

#### Implementação

10 - 11 - 2026
`0452ae0` — feat(multas): adicao de excecoes de dominio
Criei o módulo `exceptions.py` contendo as exceções puras de domínio para isolar falhas de entidade ausente e dados inválidos de pagamento.

10 - 11 - 2026
`a3fafad` — refactor(multas): adiciona validacao do valor
Adicionei a validação no `__post_init__` do Value Object `Pagamento` para impedir a instanciação com valores nulos ou negativos.

10 - 11 - 2026
`6f219b0` — refactor(multas): padronizacao do repository.py
Refatorei o `SqlAlchemyMultaRepository` e o `FakeMultaRepository` para responderem com o mesmo contrato de erro (`MultaNaoEncontrada`), corrigindo a violação de LSP.

10 - 11 - 2026
`9be867e` — refactor(multas): service_layer simplificado devido a mudanca no repository
Simplifiquei a camada de serviço `pagar_multa`, removendo a verificação procedural `if multa is None`.

10 - 11 - 2026
`a705916` — refactor(multas): atualizacao do endpoint pra tratar excecoes de dominio
Atualizei o endpoint HTTP para capturar `MultaNaoEncontrada` (HTTP 404) e `ValorPagamentoInvalido` (HTTP 400), eliminando dependências diretas de exceções do ORM (DIP).

10 - 11 - 2026
`1f18f9e` — docs(multas): documentacao da refatoracao solid adicionada
Documentei as violações de LSP e DIP, a solução aplicada, os testes de regressão e o custo da refatoração no arquivo `docs/solid.md`.

#### Arquivos

- `src/biblioteca/multas/domain/exceptions.py`
- `src/biblioteca/multas/domain/model.py`
- `src/biblioteca/multas/adapters/repository.py`
- `src/biblioteca/multas/service_layer/services.py`
- `src/biblioteca/multas/entrypoints/flask_app.py`
- `src/biblioteca/multas/tests/unit/test_multas.py`
- `docs/solid.md`

#### Testes

10 - 11 - 2026

Adicionei testes unitários para a validação de `Pagamento` e para a garantia de contrato de exceção em ambos os repositórios, além de manter os testes E2E da API verificando o retorno de HTTP 404 para multas inexistentes.

#### Decisão de projeto

10 - 11 - 2026

Padronizei a ausência de registros como exceção explícita de domínio em vez de retornar `None` ou vazar exceções do banco de dados, protegendo a camada de apresentação e unificando o contrato entre as implementações do repositório.

#### Uso de IA

Utilizei IA generativa para identificar pontos de violação de LSP/DIP no contrato do repositório e formatar o texto do `docs/solid.md`. Testei todas as alterações com pytest.

---

### Fase 2 — Checkpoint 3

#### Implementação

10 - 11 - 2026
`1fece2f` — feat(multas): implementacao do Decorator no calculo de acrescimos de multa
Implementei a interface `CalculoMulta`, o componente `CalculoMultaBase` e os decoradores `DecoradorJurosMora` e `DecoradorTaxaAdministrativa` no modelo de domínio, permitindo acréscimos dinâmicos sem alterar `Multa`.

10 - 11 - 2026
`c5ffd3c` — test(multas): adiciona testes unitarios para decoradores de juros e taxa adm
Criei os testes unitários exercitando o cálculo isolado do decorador de juros de mora e a composição encadeada com a taxa administrativa.

11 - 11 - 2026
`6873f1c` — docs(multas): documenta padrao decorator no gof.md
Documentei a aplicação do padrão estrutural Decorator no arquivo `docs/gof.md`, incluindo diagrama Mermaid, justificativa, alternativas e participantes.

#### Arquivos

- `src/biblioteca/multas/domain/model.py`
- `src/biblioteca/multas/tests/unit/test_multas.py`
- `docs/gof.md`

#### Testes

10 - 11 - 2026

Implementei testes unitários cobrindo tanto o uso isolado de `DecoradorJurosMora` quanto o aninhamento flexível de `DecoradorTaxaAdministrativa` sobre `DecoradorJurosMora`.

#### Decisão de projeto

10 - 11 - 2026

Optei pelo padrão Decorator para permitir a composição cumulativa e dinâmica de encargos (juros e taxas) sobre a multa em tempo de execução, evitando a explosão de subclasses e mantendo o modelo alinhado aos princípios SRP e OCP.

#### Uso de IA

Utilizei IA generativa para gerar a sintaxe do diagrama de classes em Mermaid e estruturar o texto no `docs/gof.md`. Testei o código e validei os cenários com pytest.

## Isabella Vieira da Motta

### Fase 1 — Checkpoint 1

#### Implementação
23-09-2026 
`2de12e2` — feat(leitores): cria Leitor e CategoriaLeitor
Implementei o agregado de Cadastro de Leitores, criando a entidade raiz `Leitor` e o Value Object `CategoriaLeitor`, encapsulando a regra de limite de empréstimos.

#### Arquivos
- `src/biblioteca/domain/model.py`

#### Testes
24-09-2026 
`70bc735` — test(leitores)
Foram implementados testes unitários para garantir que as invariantes de limite de empréstimos por categoria e a regra de leitores inativos funcionam corretamente na camada de domínio.

#### Decisão de projeto
23-09-2026 
A lógica de validação de empréstimos foi mantida estritamente na camada de domínio. Modelei `Leitor` como a raiz do agregado e `CategoriaLeitor` como um *Value Object*. Isso blinda o domínio e garante que o estado do utilizador apenas mude se as regras do produto forem respeitadas.

### Fase 1 — Checkpoint 2

#### Implementação
28-09-2026 
`a8aef88` — feat(leitores): adiciona AbstractLeitorRepository e FakeLeitorRepository
`c550652` — feat(leitores): mapeia tabelas no SQLAlchemy e implementa repositorio real
`be3b348` — fix(leitores): corrige importacao do composite no orm e declara repositorio
Implementei o mapeamento ORM com SQLAlchemy e criei os repositórios abstrato, fake (para testes) e real.

#### Arquivos
- `src/biblioteca/adapters/repository.py`
- `src/biblioteca/adapters/orm.py`
- `tests/conftest.py`

#### Testes
28-09-2026 
`09ee98a` — test(leitores): adiciona teste de integracao e config do banco em memoria[cite: 2]
Foi configurada uma base de dados em memória (`conftest.py`) e criados testes de integração para validar o contrato do `Repository` com a base de dados real[cite: 2].

#### Decisão de projeto
28-09-2026 
Optei pelo mapeamento imperativo do SQLAlchemy usando o padrão *Composite* para a `CategoriaLeitor`. Isto permitiu persistir a categoria na mesma tabela do leitor, otimizando a base de dados sem poluir as classes de domínio com detalhes de infraestrutura.

### Fase 1 — Entrega

#### Implementação
28-09-2026 
`332e5ce` — feat(leitores): implementa caso de uso para cadastro na camada de servicos
`1ff7e08` — feat(leitores): cria endpoint POST /leitores na API Flask
`68cf233` — feat(leitores): configura banco em memoria na api e adiciona testes e2e
Desenvolvi a camada de serviços para orquestrar a criação do leitor e expus a funcionalidade através de um endpoint POST na API Flask com uma base de dados temporária.

#### Arquivos
- `src/biblioteca/service_layer/services.py`
- `src/biblioteca/entrypoints/flask_app.py`
- `tests/e2e/test_leitores_api.py`

#### Testes
28-09-2026 
Foram adicionados testes End-to-End (E2E) simulando requisições HTTP diretas ao endpoint Flask utilizando o cliente de testes nativo, garantindo que a rota orquestra o caso de uso corretamente.

#### Decisão de projeto
28-09-2026 
A camada de serviço foi utilizada para orquestrar as validações e a injeção do repositório, garantindo que o endpoint Flask apenas lide com tráfego web e não contenha regras de negócio.

### Fase 2 — Checkpoint 3 (GoF)

### Fase 2 — Checkpoint 3 (GoF)

#### Implementação
10-11-2026
feat(leitores): substitui padrao State por Observer
Implementei o padrão comportamental *Observer* para permitir que efeitos colaterais (como envio de emails ou logs) reajam à inativação de um leitor, sem acoplar a entidade principal a serviços externos.
