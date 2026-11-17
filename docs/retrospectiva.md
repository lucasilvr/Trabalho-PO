# Retrospectiva da Fase 2

## 1. A pergunta

Depois de conviver com esta arquitetura, refatorar os agregados e aplicar padrões de
projeto, **nós a escolheríamos de novo?** A resposta curta é sim, mas com dois ajustes na
forma de compor e de integrar. A resposta longa está abaixo, confrontando o que o
checkpoint 1 previu com o que a Fase 2 mostrou.

## 2. As previsões do checkpoint 1 se confirmaram?

O checkpoint 1 previu três coisas: testabilidade alta, modificabilidade com domínio
independente de framework e um custo maior de código de ligação. As três se confirmaram,
mas não com o mesmo peso.

**Testabilidade — confirmado, e foi o maior ganho.** A separação entre `FakeRepository`,
`SqlAlchemyRepository` e a API permitiu refatorar o contrato de repositório do Empréstimo
(LSP/DIP) em `f275b6f`, trocando a exceção `NoResultFound` por `ItemNaoEncontrado`: os
testes existentes de comportamento continuaram válidos e o commit acrescentou um teste
unitário do contrato e outro de integração. O entrypoint apenas deixou de importar
SQLAlchemy. No fechamento da Fase 2, as três suítes passam separadas: 63 testes
unitários, 15 de integração e 20 E2E, e a CI executa cada uma em um passo próprio. Isso só
é possível porque o domínio não depende de banco nem de HTTP.

**Modificabilidade — confirmado no domínio, mais caro fora dele.** O domínio permanece
sem imports de Flask e SQLAlchemy, o que permitiu refatorações localizadas: `Livro` teve
`inativar()` dividido em validação e mutação; `Reserva` teve o prazo fixo transformado em
atributo; `Leitor` teve a regra de limites separada da entidade; `OrdemServico` deixou de
validar disponibilidade de outro agregado. Em todos esses casos, a mudança ficou no
domínio ou no serviço. Porém, a previsão de que "uma operação toca várias camadas" também
se confirmou: ao acrescentar `categoria_leitor` ao empréstimo, foram necessários domínio,
mapeamento ORM, serviço, entrypoint e quatro arquivos de teste. A camada não atrapalhou,
mas cobrou o pedágio previsto.

**Custo de ligação — subestimado.** O checkpoint 1 tratou o custo como "mais arquivos e
conceitos". Na prática, o custo maior foi a **repetição por agregado**: seis
`AbstractRepository`, seis módulos de ORM, seis aplicações Flask e seis conjuntos de
fixtures. Isso multiplicou o esforço de refatoração e trouxe um problema que não estava
previsto: o ciclo de vida dos mapeadores do SQLAlchemy (`start_mappers` e
`clear_mappers`) precisou ser acertado módulo a módulo — há commits de correção só disso
(`9567858`, `065bb5d`, `deacc77`). Foi o trade-off que mais pesou no dia a dia.

## 3. As camadas facilitaram ou atrapalharam?

**Facilitaram as refatorações de SOLID.** Os cinco princípios apareceram de forma
distribuída — SRP no Acervo, na Manutenção e nos Leitores; OCP na Reserva, no Acervo e nos
Leitores; LSP e DIP no Empréstimo e nas Multas — e cada um pôde ser resolvido dentro do
agregado, com testes na camada adequada. Sem a fronteira do repositório, a correção de LSP
no Empréstimo teria virado uma mudança no entrypoint e nos testes de API.

**Facilitaram os padrões de projeto.** A Fase 2 terminou com seis padrões diferentes, um
por integrante: Strategy no Empréstimo, Chain of Responsibility no Acervo, State na
Reserva, Decorator nas Multas, Command na Manutenção e Observer nos Leitores. Cada um
encontrou uma camada natural: Strategy e Chain na fronteira entre serviço e domínio, State
dentro da entidade, Command no serviço, Observer na entidade e no serviço. O padrão não
foi enxertado; ele resolvia um problema concreto do agregado.

**Atrapalharam em um ponto específico: a composição.** O entrypoint ainda instancia
`SqlAlchemyRepository(session)`, então a camada de entrada conhece o adapter concreto. O
checkpoint 1 já havia apontado isso; a Fase 2 confirmou que é o ponto mais frágil. O caso
do Strategy mostrou o efeito: para a política de atraso sobreviver ao recarregamento do
banco, foi preciso persistir a categoria e reconstruir a estratégia na entidade — uma
decisão que atravessou domínio, ORM, serviço e API. Funciona, mas revela que o desenho
"serviço escolhe a estratégia" e o desenho "entidade se reconstrói" precisam estar
alinhados explicitamente.

## 4. Trade-offs que mais pesaram

1. **Testabilidade x quantidade de código.** O ganho de testar serviços sem banco é real,
   mas exige manter `FakeRepository` em paralelo ao repositório SQLAlchemy.
2. **Mudança local x coordenação.** Uma alteração de domínio é local; uma funcionalidade
   ponta a ponta atravessa cinco arquivos, como no `categoria_leitor`.
3. **Mapeamento explícito x disciplina.** O mapeamento imperativo manteve o domínio puro,
   ao custo de gerenciar `start_mappers`/`clear_mappers` e de acertar o teardown dos
   mapeadores em cada módulo.
4. **Autonomia x integração.** Trabalhar em branches por integrante preservou a autonomia,
   mas concentrou merges perto dos prazos e deixou as tags dos checkpoints apontando para
   branches individuais, não para a `main`. A arquitetura não causa isso, mas também não
   protege contra isso.

## 5. Decisão final

**Manter a arquitetura em camadas com Repository Pattern e Service Layer**, com dois
ajustes — ou seja, uma decisão híbrida, não uma troca:

- **Ponto de composição explícito.** Injetar a fábrica de repositórios na aplicação, em
  vez de instanciar `SqlAlchemyRepository` dentro de cada view. Mantém o domínio
  independente e reduz o acoplamento que o checkpoint 1 já identificava.
- **Infraestrutura de teste compartilhada.** Um único módulo de suporte para criar engine,
  mapear e limpar mapeadores, eliminando a repetição que gerou os conflitos de CI.

Descartamos o **Django full-stack**: ele traria migrações, admin e autenticação, mas
faria as entidades herdarem de `models.Model`, acoplando o domínio ao framework e
inviabilizando a propriedade que mais usamos na Fase 2 — refatorar regras sem tocar em
infraestrutura. Também descartamos o **Active Record com lógica nas rotas**: seria mais
simples no começo, mas repetiria validações e dificultaria os testes isolados que
sustentaram as refatorações.

## 6. O que faríamos diferente

Integrar continuamente, com PRs pequenos e frequentes, em vez de concentrar merges nos
prazos; criar as tags dos checkpoints na `main`, depois da integração de todos; registrar
as decisões no `DECISIONS.md` no momento em que são tomadas, e não no fechamento; e
padronizar o ciclo de vida dos mapeadores do SQLAlchemy desde o primeiro agregado.

Não implementamos o experimento opcional em `experimentos/`. A comparação que embasa esta
retrospectiva veio do próprio histórico — os commits de refatoração, os padrões aplicados
e os testes que precisaram mudar (ou não) em cada etapa — e da análise de Django em
`docs/frameworks.md`. Para o tamanho do sistema, um caso de uso reimplementado em outro
estilo acrescentaria pouco à conclusão: o custo dominante não foi escrever a versão
alternativa, foi coordenar seis agregados e seis integrantes sobre a mesma `main`.
