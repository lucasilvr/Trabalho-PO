# DECISIONS

## Nota do grupo sobre as tags da Fase 2

As tags `fase2-checkpoint-2` e `fase2-checkpoint-3` foram criadas antes de todos os
trabalhos do checkpoint estarem integrados à `main` e apontam para commits da branch
de um integrante, e não para a `main`:

| Tag | Commit | Criada em |
|---|---|---|
| `fase2-checkpoint-2` | `27d0ec9` (branch `docs/fase2-checkpoint-2`) | 03/11, 23h22 |
| `fase2-checkpoint-3` | `3347127` (branch `docs/fase2-checkpoint-3`) | 05/11, 11h17 |

A tag `fase2-checkpoint-1` não foi criada.

Por isso, essas tags não contêm todos os commits do checkpoint. Para permitir a
conferência, registramos abaixo quando o trabalho de cada integrante foi integrado
à `main`, por pull request:

| Integrante | Checkpoint | Pull request / merge na `main` | Data e hora |
|---|---|---|---|
| João | CP2 | #10 — `641d2ff` | 03/11, 09h46 |
| Lucas | CP2 | #13 — `88f98d9` | 09/11, 15h34 |
| João | CP3 | #14 — `066de4f` | 10/11, 13h16 |
| Sandy | CP2 | #11 — `9bf7208` | 10/11, 20h15 |
| Sandy | CP1 | #15 — `2815017` | 10/11, 20h18 |
| Isabella | CP3 | #16 — `54f2072` | 10/11, 20h44 |
| Lucas | CP3 | #17 — `7325449` | 10/11, 22h00 |
| Isabella | CP3 | #18 — `1856741` | 11/11, 00h25 |
| Ana Laura | CP3 | #20 — `db4c281` | 11/11, 01h13 |
| Sandy | CP3 | #12 — `7d53f53` | 11/11, 01h17 |

Optamos por não apagar nem recriar as tags já publicadas, para não alterar referências
criadas dentro dos prazos. Os commits de cada integrante podem ser conferidos pelos
hashes citados nas subseções individuais. A tag `fase2-entrega` será criada na `main`,
após a integração de todos os trabalhos e com a CI verde.

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

### Fase 2 — Checkpoint 3

#### Implementação

`0a79511` — feat(emprestimo): aplica Strategy na politica de atraso

Implementei o padrão Strategy no agregado Empréstimo. Criei a interface `PoliticaAtraso`, as estratégias `SemTolerancia` e `ToleranciaEmDias` e passei `ItemEmprestado` a delegar a decisão de atraso para a política recebida. O serviço `registrar_emprestimo` seleciona a política pela categoria do leitor, mantendo `SemTolerancia` como padrão quando a categoria não é informada.

`feat(emprestimo): expoe categoria do leitor na API e documenta Strategy` (commit que acompanha esta subseção)

Expus `categoria_leitor` como campo opcional no `POST /emprestimos`, validei o tipo e passei a devolver a categoria na representação do item. Documentei o padrão em `docs/gof.md`.

#### Arquivos

- `src/biblioteca/emprestimo/domain/politicas.py`
- `src/biblioteca/emprestimo/domain/model.py`
- `src/biblioteca/emprestimo/service_layer/services.py`
- `src/biblioteca/emprestimo/adapters/orm.py`
- `src/biblioteca/emprestimo/entrypoints/flask_app.py`
- `src/biblioteca/emprestimo/tests/unit/test_politica_atraso.py`
- `src/biblioteca/emprestimo/tests/unit/test_services_emprestimo.py`
- `src/biblioteca/emprestimo/tests/integration/test_emprestimo_orm.py`
- `src/biblioteca/emprestimo/tests/e2e/test_emprestimo_api.py`
- `docs/gof.md`

#### Testes

05/11/2026

Testei a política padrão, as tolerâncias de um e de três dias, a troca de estratégia em tempo de execução, a rejeição de tolerância negativa, o item devolvido, a seleção da política pela categoria no serviço, a recarga do item a partir do banco com `expunge_all()` e o comportamento pela API HTTP, incluindo a rejeição de categoria inválida. A suíte do Empréstimo passou com `28 passed`.

#### Decisão de projeto

05/11/2026

Mantive `SemTolerancia` como política padrão e passei a persistir `categoria_leitor`, porque a revisão mostrou que uma política apenas injetada na criação se perdia quando o item era recarregado do banco. Com a categoria persistida e `politica_atraso` como property, a entidade reencontra a estratégia correta mesmo sendo reconstruída pelo SQLAlchemy sem chamar o construtor.

#### Uso de IA

Utilizei IA generativa para comparar Strategy com condicionais na entidade, Template Method e Decorator, para organizar o rascunho de `docs/gof.md` e desta subseção e para revisar a implementação. A revisão apontou que a política não sobrevivia ao reload; corrigi o desenho persistindo a categoria, verifiquei o diagrama contra as classes implementadas e executei as suítes de unidade, integração e E2E. A escolha do padrão e a responsabilidade pelo resultado final são minhas.

### Fase 2 — Entrega

#### Implementação

17 - 11 - 2026

`fa10fc0` — docs: adiciona frameworks e retrospectiva da entrega final (commit que acompanha esta subseção)

Redigi `docs/frameworks.md`, com o papel de Flask, SQLAlchemy e pytest na solução, a camada em que cada um aparece, a verificação de que o domínio não os importa, quatro pontos de inversão de controle localizados no código (registro de rotas, contexto de requisição, mapeamento ORM e fixtures do pytest), oito padrões que os frameworks usam internamente e a comparação com Django. Redigi também `docs/retrospectiva.md`, retomando as previsões do checkpoint 1, confrontando-as com as evidências da Fase 2 e registrando a decisão final de manter a arquitetura com dois ajustes.

#### Arquivos

- `docs/frameworks.md`
- `docs/retrospectiva.md`
- `DECISIONS.md`

#### Testes

17 - 11 - 2026

Executei as três suítes antes de escrever: 63 testes unitários, 15 de integração e 20 E2E, todos passando. Também confirmei por `git grep` que nenhum arquivo de domínio importa Flask, SQLAlchemy ou pytest. A `main` estava com a CI verde no commit `00cfbbb` quando comecei a documentação.

#### Decisão de projeto

17 - 11 - 2026

Escrevi a análise dos frameworks a partir de ocorrências reais no código do grupo — a rota em `flask_app.py`, o `map_imperatively` em `orm.py` e a fixture `client` nos testes E2E — em vez de descrever os frameworks em abstrato, porque o enunciado pede que os pontos de inversão de controle e os padrões sejam localizados no código do próprio grupo. A mesma escolha guiou a retrospectiva, que usa commits, testes e incidentes do repositório como evidência, e não impressões genéricas.

#### Uso de IA

Utilizei IA generativa para levantar os pontos de inversão de controle e os padrões internos dos frameworks, comparar o efeito de uma solução Django com a arquitetura em camadas e organizar os rascunhos de `docs/frameworks.md`, `docs/retrospectiva.md` e desta subseção. Conferi cada referência de arquivo e linha no código, executei as três suítes e ajustei o texto e as conclusões; a decisão final de manter a arquitetura e a responsabilidade pelo conteúdo são minhas.

#### Reflexão

A Fase 2 mudou a forma como eu leio o meu próprio código. No checkpoint 2, ao procurar uma violação de LSP no Empréstimo, percebi que o problema não estava na exceção em si, mas no contrato: duas implementações do mesmo repositório reagiam de formas diferentes ao mesmo caso, e o entrypoint precisava conhecer o SQLAlchemy para traduzir o erro. Trocar isso por `ItemNaoEncontrado` foi simples justamente porque o domínio já estava isolado; a camada não atrapalhou, ela mostrou onde o acoplamento estava. No checkpoint 3, o Strategy me ensinou algo que eu não tinha previsto: um padrão pode estar correto e ainda assim não funcionar de ponta a ponta. A política era escolhida na criação e se perdia quando o item era recarregado do banco. Só descobri isso ao escrever um teste que recarregava o objeto de verdade; a correção exigiu persistir a categoria e mudou quatro camadas. Aprendi que testar o caminho real, e não só o objeto em memória, é o que separa um padrão decorativo de um padrão útil. O que eu faria diferente é o processo: integrar antes, abrir PR cedo e criar as tags na `main` no dia do prazo. Concentrei commits e merges no fim, e as tags acabaram apontando para branches individuais. Também declararia cada uso de IA no momento em que acontece.

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

### Fase 2 — Checkpoint 1

> **Nota:** As descrições de cada etapa representam o que era esperado para cada checkpoint do projeto. Como o desenvolvimento da minha parte foi realizado em um período de tempo reduzido, várias atividades foram executadas em paralelo para garantir o atendimento dos requisitos mínimos da solução. Dessa forma, as evidências não demonstram necessariamente uma evolução cronológica entre os checkpoints. A organização foi feita considerando o escopo entregue em cada etapa, e não o momento exato em que cada implementação foi realizada.

#### Implementação

Inicialmente, o construtor da entidade verificava tanto se o dano era reparável quanto se havia um exemplar disponível. Como a disponibilidade está relacionada ao módulo de Acervo, essa responsabilidade foi transferida para a camada de serviço, mantendo na entidade apenas a validação referente à reparabilidade do dano.

`6567a64` - Foi elaborado um ADR para registrar a decisão de separar a validação da disponibilidade do exemplar da entidade OrdemServico.

#### Arquivos
`docs/adr/0006-validacao-disponibilidade-ordem-servico.md`

#### Decisão de projeto
A decisão foi separar as responsabilidades entre os módulos, reduzindo o acoplamento entre Manutenção e Acervo e tornando a entidade OrdemServico mais coesa.

### Fase 2 — Checkpoint 2

#### Implementação
`5e0d902` - Foi realizada uma refatoração no módulo de Manutenção para atender ao princípio SRP (Single Responsibility Principle). A validação da disponibilidade do exemplar foi transferida para `OrdemServicoService`, deixando a entidade responsável apenas pelas regras relacionadas à ordem de serviço.

#### Arquivos
- `src/biblioteca/manutencao/domain/model.py`
- `src/biblioteca/manutencao/service_layer/services.py`
- `docs/solid.md`

#### Testes
Após a refatoração, foram executados os testes do módulo de Manutenção, com aprovação dos 10 testes existentes.

#### Decisão de projeto
A mudança buscou respeitar o princípio da responsabilidade única, evitando que a entidade de Manutenção assumisse uma responsabilidade pertencente ao contexto de Acervo.

### Fase 2 — Checkpoint 3

#### Implementação
`627174f` - Foi implementado o padrão comportamental Command no módulo de Manutenção, utilizando a conclusão de uma ordem de serviço como operação encapsulada.

Foi criada a classe abstrata `Command`, com o método `execute()`, e sua implementação concreta `ConcluirOrdemServicoCommand`. A classe recebe uma ordem de serviço e executa sua conclusão por meio do método `concluir()` da entidade.
A integração foi realizada em `OrdemServicoService`, que recupera a ordem de serviço, verifica sua existência e delega a operação ao comando.

`d67db1c` - A implementação e a justificativa da escolha foram registradas em `docs/gof.md`, incluindo a estrutura do padrão, seus participantes e os testes realizados.

#### Arquivos
`src/biblioteca/manutencao/service_layer/commands.py`
`src/biblioteca/manutencao/service_layer/services.py`
`src/biblioteca/manutencao/tests/unit/test_manutencao.py`

#### Testes
`627174f` - Foram adicionados dois testes unitários:
- Verificação da conclusão de uma ordem de serviço por meio do `Command`.
- Verificação de que uma ordem de serviço que não está em execução não pode ser concluída.

Após a implementação, os 12 testes do módulo de Manutenção foram executados com sucesso.

#### Decisão de projeto
O padrão Command foi escolhido por permitir encapsular a operação de conclusão de uma ordem de serviço em um objeto próprio, separando a solicitação da execução da ação.

A escolha também considerou a necessidade de utilizar um padrão GoF diferente dos demais integrantes do grupo.

### Fase 2 — Entrega

#### Consolidação das atividades
Foram concluídas as atividades referentes à refatoração SOLID e à implementação do padrão GoF no módulo de Manutenção e Conservação do Acervo.
Também foi elaborado um ADR para registrar a decisão arquitetural relacionada à separação das responsabilidades entre os módulos de Manutenção e Acervo.

#### Arquivos entregues
`docs/solid.md`
`docs/gof.md`
`docs/adr/0006-validacao-disponibilidade-ordem-servico.md`
`src/biblioteca/manutencao/domain/model.py`
`src/biblioteca/manutencao/service_layer/services.py`
`src/biblioteca/manutencao/service_layer/commands.py`
`src/biblioteca/manutencao/tests/unit/test_manutencao.py`

#### Uso de IA
A IA foi utilizada como ferramenta de apoio durante o desenvolvimento, principalmente para auxiliar na compreensão dos princípios SOLID e dos padrões GoF, além de apoiar na avaliação de alternativas de implementação e revisão de trechos de código ou documentação.

As sugestões foram avaliadas e adaptadas ao contexto do projeto. Todas as decisões de arquitetura, implementação e validação permaneceram sob minha responsabilidade, sendo a solução verificada por meio da execução dos testes automatizados.

#### Reflexão
A atividade permitiu aprofundar a compreensão sobre a importância da separação de responsabilidades e da organização do código em camadas.
A refatoração SRP evidenciou como uma entidade pode acabar assumindo responsabilidades de outro módulo, aumentando o acoplamento entre os contextos do sistema.

Já a implementação do Command demonstrou como uma operação pode ser encapsulada, tornando sua execução mais organizada e permitindo separar a lógica de solicitação da ação propriamente dita.
Um dos principais aprendizados foi perceber que a aplicação de padrões de projeto deve partir de uma necessidade concreta do sistema, e não apenas da intenção de utilizar determinado padrão.

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

29 - 10 - 2026
`9054433` — feat: adiciona documentos ADR e modelagem do livro

Documentei, em conjunto com a Ana Laura, as decisões arquiteturais dos módulos de Acervo (`docs/adr/0002-modelagem-livro-exemplar.md`) e de Penalidades (`docs/adr/0003-api-flask-multas.md`). No commit `9054433`, adicionei o arquivo `0003-api-flask-multas.md` e revisei o arquivo `0002-modelagem-livro-exemplar.md` (que trata da separação entre `Livro` e `Exemplar` no Acervo), confirmando o status como "Aceita".

#### Observação sobre a autoria dos ADRs

Os ADRs do checkpoint 1 dos módulos de Acervo e de Penalidades foram escritos por mim e pela Ana Laura trabalhando juntos. Na hora de commitar, os arquivos acabaram invertidos: cada um commitou o ADR do módulo do outro.

- `docs/adr/0002-modelagem-livro-exemplar.md` (Acervo, meu módulo): commitado pela Ana Laura em `fed5d51` (23/10/2026). Depois, no meu commit `9054433` (29/10/2026),
conferi o texto com a implementação do Acervo, confirmei o status como "Aceita" e removi a observação que pedia essa conferência.
- `docs/adr/0003-api-flask-multas.md` (Penalidades, módulo da Ana Laura): commitado por mim em `9054433` (29/10/2026).

Como o conteúdo foi produzido em conjunto, considero o ADR 0002 como o do meu módulo.

#### Arquivos

- `docs/adr/0002-modelagem-livro-exemplar.md`
- `docs/adr/0003-api-flask-multas.md`
- `DECISIONS.md`

#### Testes

29 - 10 - 2026

Conferi as decisões documentadas em relação à implementação existente do módulo de Acervo (`src/biblioteca/acervo/domain/model.py` e `adapters/orm.py`) e do módulo de Penalidades, bem como às verificações automatizadas do projeto.

#### Decisão de projeto

29 - 10 - 2026

Mantive `Livro` e `Exemplar` como conceitos separados no domínio do Acervo (e a API HTTP separada das regras de domínio e da camada de serviço), pois isso permite controlar o estado físico de cada exemplar individualmente sem misturar regras de negócio com protocolo HTTP ou detalhes de persistência.

#### Uso de IA

Utilizei IA generativa principalmente para compreender melhor os conceitos de ADR e de documentação arquitetural cobrados na disciplina, entender o fluxo do que precisava ser entregue no checkpoint e organizar a estrutura textual do documento. Conferi o conteúdo em relação ao código real do repositório, assumindo a responsabilidade pela versão final.

### Fase 2 — Checkpoint 2

#### Implementação

29 - 10 - 2026
`af2da29` — feat: aplica principio de responsabilidade unica
`de3107a` / `dc0ac0f` — feat: separa validacao de inativacao do dominio

Refatorei a entidade `Livro` em `src/biblioteca/acervo/domain/model.py` (cujo código original vinha do commit `ecce5f6`, de 20/09/2026) aplicando o Princípio da Responsabilidade Única (SRP). Antes, o método `inativar()` fazia o laço de verificação dos exemplares, disparava a exceção e alterava o estado no mesmo lugar. Separei esse comportamento em três métodos distintos: `pode_ser_inativado()`, `validar_inativacao()` e `inativar()`, além de adicionar `clear_mappers()` e verificação de mapeamento existente em `src/biblioteca/acervo/adapters/orm.py`.

02 - 11 - 2026
`54ce4dc` — fix: separa validacao de inativacao e ajusta mapeamento orm
`2fc2eea` — feat: add analise solid e testes service layer

Ajustei o mapeamento imperativo da relação `exemplares` em `orm.py`, evoluí `src/biblioteca/acervo/service_layer/services.py` (`adicionar_livro`, `listar_livros` e `inativar_livro`) mantendo a dependência na abstração `AbstractRepository` (DIP), criei os testes unitários da camada de serviço em `src/biblioteca/acervo/tests/unit/test_services_acervo.py` e registrei a análise em `docs/solid.md`.

#### Arquivos

- `src/biblioteca/acervo/domain/model.py`
- `src/biblioteca/acervo/adapters/orm.py`
- `src/biblioteca/acervo/service_layer/services.py`
- `src/biblioteca/acervo/tests/unit/test_services_acervo.py`
- `docs/solid.md`

#### Testes

02 - 11 - 2026

Os testes da Fase 1 (`test_acervo.py`, `test_repository.py` e `test_api.py`) continuaram passando sem alteração, garantindo que o comportamento existente não quebrou. Adicionei 3 novos testes unitários em `test_services_acervo.py` usando `FakeRepository` e `DummySession` para validar a adição de livros, a inativação e o erro ao tentar inativar um livro inexistente.

#### Decisão de projeto

02 - 11 - 2026

Optei por dividir o método `inativar()` em `pode_ser_inativado()`, `validar_inativacao()` e `inativar()` porque separar a consulta booleana da validação e da mudança de estado deixa cada método com uma única responsabilidade e permite reutilizar a checagem de disponibilidade sem precisar alterar o estado do livro.

#### Uso de IA

Utilizei IA generativa mais para estudar e entender como os princípios SOLID (especialmente SRP, OCP e DIP) se aplicavam na prática ao meu agregado, entender o fluxo do trabalho pedido no checkpoint e tirar dúvidas sobre recursos e sintaxe da linguagem Python (como `any()`, compreensões de gerador e funcionamento do `pytest`), já que não tenho tanta familiaridade com Python no dia a dia. Não usei a IA para gerar o trabalho inteiro de forma automática; fui entendendo o fluxo, implementando, testando e revisando cada ajuste.

#### Integração na `main`

Os commits deste checkpoint foram integrados à `main` pelo PR #13 (`88f98d9`, 09/11, 15h34). Ver a nota do grupo sobre as tags no início do documento.

### Fase 2 — Checkpoint 3

#### Implementação

09 - 11 - 2026
`57125a2` — feat: aplica chain of responsibility na validacao de livros

Implementei o padrão GoF comportamental **Chain of Responsibility** no módulo de Acervo. Criei `src/biblioteca/acervo/service_layer/validators.py` com o handler `ValidadorCampoLivro` e as funções `criar_cadeia_validacao_livro()` e `criar_cadeia_validacao_isbn()`, encadeando a validação e normalização (`strip()`) dos campos `isbn`, `titulo` e `autor`. Atualizei `src/biblioteca/acervo/service_layer/services.py` para usar a cadeia antes de instanciar ou buscar o `Livro` e criei os testes unitários em `src/biblioteca/acervo/tests/unit/test_validators.py`.

09 - 11 - 2026
`6787a54` — doc: gof.md

Documentei a aplicação do padrão Chain of Responsibility em `docs/gof.md`, incluindo contexto, tabela de participantes, diagrama em Mermaid e descrição dos testes.

10 - 11 - 2026
`40f3ccb` — fix: corrige ci de cadastro isolando os mapeadores orm

Ajustei o isolamento dos mapeadores ORM (`clear_mappers`) durante a integração na `main` para resolver o conflito entre testes na pipeline de CI.

#### Arquivos

- `src/biblioteca/acervo/service_layer/validators.py`
- `src/biblioteca/acervo/service_layer/services.py`
- `src/biblioteca/acervo/tests/unit/test_validators.py`
- `docs/gof.md`
- `src/biblioteca/cadastro/adapters/orm.py`
- `src/biblioteca/cadastro/tests/conftest.py`
- `src/biblioteca/cadastro/tests/e2e/test_leitores_api.py`

#### Testes

09 - 11 - 2026

Foram criados os testes unitários em `test_validators.py` verificando que a cadeia valida e remove espaços extras dos três campos obrigatórios e que qualquer campo vazio interrompe a cadeia lançando `ValueError` (exercitado com `@pytest.mark.parametrize` para ISBN, título e autor). Todos os testes do módulo Acervo (`12 passed`) e da CI continuaram passando.

#### Decisão de projeto

09 - 11 - 2026

Escolhi aplicar o padrão Chain of Responsibility na validação de entrada do serviço (`ValidadorCampoLivro`) em vez de manter chamadas de validação fixas dentro de `adicionar_livro`, porque isso desacopla cada etapa de validação e permite encadear novas regras para o cadastro de livros sem modificar o fluxo principal do serviço.

#### Uso de IA

Utilizei IA generativa principalmente para entender melhor o funcionamento dos padrões GoF (e como o Chain of Responsibility se encaixava no problema de validação do Acervo), tirar dúvidas sobre a sintaxe de tipagem, dicionários e `@pytest.mark.parametrize` em Python — linguagem com a qual tenho menos costume — e ajudar a montar a sintaxe do diagrama Mermaid para o `docs/gof.md`. A implementação e a conferência com os testes foram acompanhadas e validadas por mim.

#### Integração na `main`

Os commits deste checkpoint foram integrados à `main` pelo PR #17 (`7325449`, 10/11, 22h00). Ver a nota do grupo sobre as tags no início do documento.

### Fase 2 — Entrega

#### Implementação

17 - 11 - 2026
`docs(acervo): padroniza solid.md e finaliza autorrelato da Fase 2 no DECISIONS` e `docs(acervo): complementa analise de frameworks com exemplos do Acervo` (commits que acompanham esta subseção)

Em conjunto com a Sandy, contribuí em `docs/frameworks.md` localizando no agregado de Acervo o papel de Flask, SQLAlchemy e pytest, os pontos de inversão de controle (extração do parâmetro `<isbn>` nas rotas Flask, instrumentação `_sa_class_manager` e mapeamento imperativo `1:N` entre `Livro` e `Exemplar` no SQLAlchemy, fixture `session` com `clear_mappers()` e `@pytest.mark.parametrize` no pytest), os padrões internos usados pelos frameworks (Decorator, Registry, Strategy, Unit of Work / Factory Method, Proxy e Template Method) e os impactos que o uso do Django traria para o modelo de domínio do Acervo. Além disso, padronizei a seção do agregado de Acervo em `docs/solid.md` para o formato unificado do documento (`## Lucas Dias Silveira — Acervo`, mantendo o título geral `# Refatorações SOLID — Fase 2` no topo e incluindo os hashes de antes e depois, trechos de código, testes e custo da refatoração), complementei a seção do Acervo em `docs/gof.md` e `docs/adr/0002-modelagem-livro-exemplar.md`, e finalizei todas as subseções da Fase 2 (incluindo o esclarecimento sobre a autoria dos ADRs nos commits `fed5d51` e `9054433`, os relatos dos checkpoints 2 e 3 e a reflexão final) neste `DECISIONS.md`.

#### Arquivos

- `docs/frameworks.md`
- `DECISIONS.md`
- `docs/solid.md`
- `docs/gof.md`
- `docs/adr/0002-modelagem-livro-exemplar.md`

#### Testes

17 - 11 - 2026

Executei as três suítes de testes configuradas na CI (`unit`, `integration` e `e2e`), confirmando que todos os testes do repositório continuam passando.

#### Decisão de projeto

17 - 11 - 2026

Padronizei a documentação de SOLID e GoF do módulo de Acervo seguindo a mesma estrutura das demais seções do grupo, garantindo que os hashes dos commits de antes e depois e a explicação sobre a autoria cruzada dos ADRs no Checkpoint 1 fiquem explícitos para conferência no histórico do Git, e documentei em `docs/frameworks.md` os pontos concretos de inversão de controle e padrões internos que ocorrem nos adapters, entrypoints e testes do Acervo.

#### Uso de IA

Ao longo da Fase 2, utilizei IA generativa principalmente para entender melhor os conteúdos teóricos da disciplina (princípios SOLID, padrões de projeto GoF, ADRs e arquitetura em camadas), compreender o fluxo do que precisava ser feito em cada etapa do trabalho e tirar dúvidas sobre a linguagem Python, já que não mexo tanto com Python no dia a dia. Não utilizei a IA para fazer o código totalmente por conta própria, mas sim como apoio para entender a linguagem e estruturar e revisar os textos de documentação e deste `DECISIONS.md`, assumindo total responsabilidade pelo resultado final.

#### Reflexão

Realizar a Fase 2 no módulo de Acervo me ajudou muito a enxergar na prática conceitos de engenharia de software que antes pareciam apenas teóricos. Na Fase 1, meu foco principal tinha sido fazer o código funcionar nas camadas exigidas, mesmo sem ter tanta familiaridade com Python. Quando precisei revisitar o próprio código na Fase 2 para aplicar SOLID, percebi que o método `inativar()` da classe `Livro` fazia coisas demais ao mesmo tempo: percorria os exemplares, decidia se lançava erro e alterava o atributo `ativo`. Dividir essa lógica em `pode_ser_inativado()`, `validar_inativacao()` e `inativar()`, junto com os testes unitários da camada de serviço usando `FakeRepository`, deixou o código muito mais claro e seguro de mexer. Da mesma forma, aplicar o padrão *Chain of Responsibility* (`ValidadorCampoLivro`) no Checkpoint 3 mostrou como organizar validações em cadeia evita poluir o serviço `adicionar_livro` com várias verificações seguidas. Outro aprendizado importante foi entender o papel dos frameworks e da inversão de controle, principalmente quando enfrentamos erros de mapeadores duplicados do SQLAlchemy na CI e precisei entender como `start_mappers()` e `clear_mappers()` funcionavam por trás dos panos. O que eu faria diferente seria distribuir melhor os commits ao longo das semanas para não concentrar entregas perto do prazo, ter mais atenção no momento de commitar arquivos feitos em dupla (como ocorreu na troca dos ADRs com a Ana Laura no Checkpoint 1) e atualizar o `DECISIONS.md` imediatamente após cada PR.

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

#### Uso de IA (declaração feita em 13/11/2026)

Na Fase 1, a regra da disciplina não permitia gerar código com IA. Declaro que, em 29/09/2026, usei o Claude (Claude Code) para resolver os conflitos de merge e reorganizar o módulo em `src/biblioteca/reservas/` (`8e5972d`) e que a IA gerou a camada de serviço, a API Flask, o `FakeFilaEsperaRepository`, os testes de integração e e2e, a igualdade por identidade das entidades e o texto desta subseção de Entrega (commits `0fc1ab3`, `eebeb34`, `6cdca3f`, `2a2e178`, `1af9fe2`, `22aaf6f`, `06e011b`, `fb7a001` e `6dd3193`). São de minha autoria, sem IA, o domínio (`Reserva` e `FilaEspera`), o mapeamento ORM, o repositório original e os testes iniciais (`f185330`, `99b7408`, `2496e8f` e `75a7802`). Faço esta declaração para que a autoria da Fase 1 fique registrada corretamente.

### Fase 2 — Checkpoint 1

#### Implementação

Não entreguei o checkpoint 1 dentro do prazo (22/10/2026). O ADR que deveria fazer parte dele foi escrito depois, na entrega final:

13 - 11 - 2026
`c828810` — docs(reservas): adiciona ADR sobre persistencia da Reserva pela FilaEspera

O ADR registra a decisão da Fase 1 de persistir as reservas apenas pela raiz `FilaEspera`.

#### Arquivos

- `docs/adr/0005-persistencia-reserva-pela-fila-espera.md`

#### Decisão de projeto

13 - 11 - 2026

Escolhi registrar no ADR a decisão de não criar um repositório para a `Reserva`, porque é a decisão que mais influenciou o restante do agregado: a refatoração OCP e o padrão State foram feitos sem mudar o repositório.

#### Uso de IA

Utilizei o Claude para redigir o ADR a partir da decisão descrita no meu autorrelato do checkpoint 2 da Fase 1. Revisei o texto e sou responsável pelo conteúdo.

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

Utilizei o Claude para analisar o código do agregado, sugerir a violação de OCP, implementar a refatoração, escrever os novos testes e redigir um rascunho de `docs/solid.md` e desta subseção. Revisei o diff, rodei a suíte de testes antes de commitar e ajustei o texto, sendo responsável pelo resultado final.

#### Integração na `main`

Os commits deste checkpoint foram integrados à `main` pelo PR #10 (`641d2ff`, 03/11, 09h46). Ver a nota do grupo sobre as tags no início do documento.

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

Utilizei o Claude para sugerir o padrão State, implementar as classes de estado e a delegação na `Reserva`, escrever os testes e redigir os rascunhos de `docs/gof.md` (incluindo o diagrama Mermaid) e desta subseção. Revisei o código e os textos, rodei a suíte de testes antes de cada commit e sou responsável pelo resultado final.

#### Integração na `main`

Os commits deste checkpoint foram integrados à `main` pelo PR #14 (`066de4f`, 10/11, 13h16). Ver a nota do grupo sobre as tags no início do documento.

### Fase 2 — Entrega

#### Implementação

13 - 11 - 2026
`c828810` — docs(reservas): adiciona ADR sobre persistencia da Reserva pela FilaEspera

15 - 11 - 2026
`5f7b956` — docs: adiciona tabela Quem faz o que e nota do grupo sobre as tags

Transformei a lista da equipe no `README.md` na tabela "Quem faz o quê" exigida pelo enunciado e escrevi, no início deste documento, a nota do grupo que registra quando o trabalho de cada integrante foi integrado à `main`, já que as tags dos checkpoints 2 e 3 não apontam para a `main`.

16 - 11 - 2026
docs(reservas): registra autorrelato da entrega final (commit que acompanha esta subseção)

Acrescentei a subseção do checkpoint 1, a declaração de uso de IA da Fase 1, as referências de integração dos checkpoints 2 e 3 e esta subseção.

17 - 11 - 2026
Ajustes finais antes da entrega:

- `8c08ce5` — docs(reservas): ajusta declaracoes de uso de IA e reflexao no DECISIONS. Corrigi as declarações de uso de IA dos checkpoints 2 e 3 para descrever com exatidão o que foi feito com o Claude e reescrevi trechos da reflexão.
- `571092d` — test(reservas): verifica persistencia dos estados da Reserva no banco. Dois testes de integração mostram que uma reserva carregada do banco volta ao estado correto do padrão State e que as transições são gravadas na coluna `status`.
- `5f412bb` — docs: remove titulos duplicados do gof.md, que tinham sobrado dos merges.
- `f4be9e6` — docs: adiciona ADR sobre a estrutura do pacote por agregado (`docs/adr/0007-estrutura-por-agregado.md`), registrando por que o grupo repete as camadas do Apêndice B dentro de cada agregado.
- `dc3405b` — docs: adiciona estrutura do repositorio e execucao dos testes ao README.

#### Arquivos

- `docs/adr/0005-persistencia-reserva-pela-fila-espera.md`
- `docs/adr/0007-estrutura-por-agregado.md`
- `docs/gof.md`
- `src/biblioteca/reservas/tests/integration/test_reserva_repository.py`
- `README.md`
- `DECISIONS.md`

#### Decisão de projeto

15 - 11 - 2026

Optei por não apagar nem recriar as tags dos checkpoints 2 e 3. Qualquer commit escolhido deixaria de fora o trabalho de algum integrante, e as tags novas teriam data posterior aos prazos. Registrar os merges com hash e horário permite conferir a entrega de cada um sem alterar referências já publicadas.

#### Uso de IA

Utilizei o Claude para levantar no histórico os horários de merge de cada pull request, redigir a nota do grupo sobre as tags, montar a tabela do `README.md` e redigir os rascunhos desta subseção e do parágrafo de reflexão, que revisei e ajustei. Sou responsável pelo resultado final.

Nos ajustes finais de 17/11, também utilizei o Claude para escrever os dois testes de integração do padrão State, redigir o ADR 0007 e as seções novas do `README.md`, remover os títulos duplicados do `docs/gof.md` e corrigir as declarações de uso de IA dos checkpoints 2 e 3. Revisei as alterações e rodei a suíte de testes antes dos commits.

#### Reflexão

A Fase 2 mudou a forma como eu enxergo o código que eu mesmo escrevi. Na Fase 1, a `Reserva` parecia simples: três métodos curtos e um prazo fixo de 48 horas. Ao procurar uma violação de SOLID, percebi que esse número fixo impedia uma mudança de requisito bem plausível, como prazos diferentes por categoria de leitor, e que bastava transformá-lo em atributo para fechar a classe para modificação. No checkpoint 3, ao aplicar o padrão State, descobri um problema que eu nunca tinha notado: uma reserva expirada podia voltar a ficar disponível, e uma reserva disponível podia ter o prazo reiniciado. Os testes que escrevi para mostrar o problema falharam no código antigo, e isso me mostrou na prática que um padrão de projeto só vale a pena quando resolve um problema real do domínio. Também entendi melhor o papel dos testes como rede de segurança: as duas refatorações foram feitas sem alterar nenhum teste existente, e foi isso que me deu confiança de que o comportamento foi preservado. O que eu faria diferente é a organização do tempo. Atrasei o checkpoint 1 e concentrei commits perto dos prazos. Por fim, combinaria com o grupo, desde o começo, quem cria as tags e quando, para que elas sempre apontem para a `main` com o trabalho de todos.


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

23 - 10 - 2026

`fed5d51` — docs: adiciona adr do acervo e registra decisions

Documentei, em conjunto com o Lucas, as decisões arquiteturais dos módulos de Acervo (`docs/adr/0002-modelagem-livro-exemplar.md`) e de Penalidades (`docs/adr/0003-api-flask-multas.md`). No commit `fed5d51`, adicionei o arquivo `0002-modelagem-livro-exemplar.md`.

#### Observação sobre a autoria dos ADRs

Os ADRs do checkpoint 1 dos módulos de Penalidades e de Acervo foram escritos por mim e pelo Lucas trabalhando juntos. Na hora de commitar, os arquivos acabaram invertidos: cada um commitou o ADR do módulo do outro.

- `docs/adr/0003-api-flask-multas.md` (Penalidades, meu módulo): commitado pelo Lucas em `9054433` (29/10/2026).
- `docs/adr/0002-modelagem-livro-exemplar.md` (Acervo, módulo do Lucas): commitado por mim em `fed5d51` (23/10/2026) e depois revisado pelo Lucas em `9054433`.

Como o conteúdo foi produzido em conjunto, considero o ADR 0003 como o do meu módulo.

#### Arquivos

- `docs/adr/0002-modelagem-livro-exemplar.md`
- `DECISIONS.md`

#### Testes

23 - 10 - 2026

Conferi a decisão documentada em relação à implementação existente do Acervo e às verificações automatizadas do projeto.

#### Decisão de projeto

23 - 10 - 2026

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

---

### Fase 2 — Entrega

#### Implementação

17 - 11 - 2026
`<24f37cf>` — docs(retrospectiva): adiciona evidencias e trade-offs do modulo de multas

Complementei o documento `docs/retrospectiva.md` inserindo as evidências práticas do módulo de Multas nas análises de modificabilidade, refatorações SOLID (`6f219b0` e `a705916`) e composição do padrão Decorator (`1fece2f`). Também atualizei o `DECISIONS.md` com o esclarecimento de autoria do ADR 0002 (`fed5d51` e `9054433`) e a reflexão final da Fase 2.

#### Arquivos

- `docs/retrospectiva.md`
- `DECISIONS.md`

#### Decisão de projeto

17 - 11 - 2026

Optamos na retrospectiva final por manter a arquitetura em camadas com Repository Pattern e Service Layer, recomendando como evoluções a injeção explícita da fábrica de repositórios na composição e o compartilhamento de fixtures de mapeamento ORM para reduzir a repetição entre agregados.

#### Uso de IA

Utilizei IA generativa para revisar a coerência textual das inserções em `docs/retrospectiva.md` e estruturar esta subseção do `DECISIONS.md`. Todos os hashes de commits, evidências técnicas do módulo de Multas e a reflexão final foram conferidos e validados por mim no repositório.

#### Reflexão

Ao longo da Fase 2, pude enxergar o código desenvolvido na Fase 1 sob uma perspectiva arquitetural muito mais crítica. Na primeira etapa, o foco estava em fazer os testes passarem e isolar o domínio usando mapeamento imperativo e repositórios; já nesta fase, percebi na prática como abstrações mal definidas cobram seu preço. A refatoração de SOLID no módulo de Multas mostrou que retornar valores nulos ou vazar exceções do SQLAlchemy quebrava a substituibilidade entre repositórios e acoplava a API Flask à infraestrutura. Da mesma forma, aplicar o padrão Decorator para calcular juros de mora e taxas administrativas evidenciou como a composição permite estender regras de negócio sem inflar a entidade principal com condicionais. Por outro lado, ficou claro o custo dessa arquitetura em camadas para um domínio relativamente simples: cada pequena evolução exige tocar múltiplos arquivos entre domínio, adaptadores, serviços e testes. Se começasse o projeto novamente, manteria a separação entre domínio e persistência nas regras financeiras críticas, mas evitaria camadas intermediárias desnecessárias nos fluxos puramente cadastrais. Além disso, eu padronizaria desde o início as exceções de domínio, os nomes dos arquivos de teste e a configuração de e-mail do Git, garantindo um histórico limpo, rastreável e com a suíte automatizada sempre verde desde os primeiros commits.

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
Foi configurada uma base de dados em memória (`conftest.py`) e criados testes de integração para validar o contrato do `Repository` com a base de dados

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

## Isabella Vieira da Motta

### Fase 2 — Checkpoint 1

#### Implementação
16-11-2026
`d1d42f7` — chore(leitores): sincroniza com a main, remove docs indevidos, renomeia adr e move testes
Elaborei a documentação da decisão arquitetural (ADR 0004) referente à separação de responsabilidades no módulo de Leitores. A decisão focou em isolar as regras de negócio de limite de empréstimos no Value Object `CategoriaLeitor`.

#### Arquivos
- `docs/adr/0004-encapsulamento-categoria-leitor.md`

#### Testes
16-11-2026
Revisei e movi os testes unitários da Fase 1 (`test_leitores.py` para a pasta `unit`) para garantir que a documentação arquitetural proposta refletia fielmente o comportamento implementado e validado pela integração contínua (CI).

#### Decisão de projeto
16-11-2026
Formalizei a decisão de encapsular as regras no Value Object para proteger a entidade raiz (`Leitor`). Isso garante que a entidade principal foque apenas na sua identidade e ciclo de vida, sem se acoplar a regras de limite que podem mudar no futuro (respeitando o Princípio de Responsabilidade Única).

#### Uso de IA
Utilizei IA generativa para debater o uso de Value Objects e auxiliar na revisão gramatical do ADR. Todo o texto foi validado manualmente.


### Fase 2 — Checkpoint 2

#### Implementação
16-11-2026
`ca8bc8d` — docs(leitores): corrige autorrelato e finaliza solid/gof
Documentei a aplicação e refatoração do módulo com base nos princípios SOLID, com foco específico no SRP (Single Responsibility Principle) através do uso do VO `CategoriaLeitor`, e preparo para o OCP (Open/Closed Principle) na ação de inativação do usuário.

#### Arquivos
- `docs/solid.md`

#### Testes
16-11-2026
Garantia de que os testes E2E e de repositório continuavam passando sem depender de lógicas procedurais rígidas na camada de serviços. 

#### Decisão de projeto
16-11-2026
Optei por registrar analiticamente como a estrutura de objetos já desenhada preparava terreno para estender comportamentos, fundamentando a necessidade de refatorar o método de inativação (que estava engessado) para o Checkpoint seguinte.

#### Uso de IA
Utilizei Claude e Gemini para analisar o código em busca de violações SOLID, o que ajudou a identificar a quebra do OCP e a formatar o documento `solid.md`.


### Fase 2 — Checkpoint 3 (GoF)

#### Implementação
10-11-2026
`a86ffe1` — refactor(leitores): substitui padrao State por Observer e atualiza documentacao
Substituí o padrão *State* pelo padrão comportamental *Observer* no ciclo de inativação de leitores. Adicionei a interface abstrata `LeitorObserver`, transformando a entidade `Leitor` num *Subject* que notifica sistemas externos sem os conhecer.

#### Arquivos
- `src/biblioteca/cadastro/domain/model.py`
- `src/biblioteca/cadastro/adapters/orm.py`
- `src/biblioteca/cadastro/tests/unit/test_leitor_observer.py`
- `docs/gof.md`

#### Testes
10-11-2026
Implementei o arquivo `test_leitor_observer.py` contendo o `MockEmailObserver` isolado. Os testes garantem que o estado do observador (mock) é alterado para "notificado" quando o método `inativar()` do leitor é chamado, mantendo a cobertura total sem quebrar o mapeamento do SQLAlchemy.

#### Decisão de projeto
10-11-2026
Optei pelo *Observer* em detrimento do *State* para focar no desacoplamento. O Observer permite que novos efeitos colaterais pós-inativação (como enviar e-mails ou cancelar reservas) sejam adicionados futuramente apenas criando novos observadores, mantendo a classe central intocada (OCP).

#### Uso de IA
Utilizei o Gemini para debater a troca do padrão State para Observer e auxiliar com o mapeamento ORM. Adaptei e testei todo o código.