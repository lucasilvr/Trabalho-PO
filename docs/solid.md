# Refatorações SOLID — Fase 2

Este documento registra as violações de SOLID encontradas no código da Fase 1 e as
refatorações feitas na Fase 2. Cada integrante documenta a sua própria refatoração,
no agregado ou módulo sob sua responsabilidade. O grupo deve cobrir, somadas as
seções, pelo menos três princípios diferentes.

## Lucas Dias Silveira — Acervo

### Princípios violados

- **Single Responsibility Principle (SRP):** Na Fase 1, o método `Livro.inativar()` concentrava em um único ponto a verificação de disponibilidade dos exemplares (`for exemplar in self.exemplares`), a validação da regra com lançamento de exceção e a mutação de estado (`self.ativo = False`).
- **Open/Closed Principle (OCP) e Dependency Inversion Principle (DIP):** A regra de negócio ficava presa dentro do método de mutação `inativar()`, impedindo consultar se um livro podia ser inativado ou estender a validação sem tentar alterar o estado da entidade. Além disso, a camada de serviço (`services.py`) dependia da abstração `AbstractRepository`, mas ainda não contava com testes unitários isolados com `FakeRepository` e sessão em memória.

### Código antes

Introduzido nos commits da Fase 1 `ecce5f6` (20/09/2026, domínio) e `18c976d` (29/09/2026, serviço), anteriores a 06/10/2026:

```python
# src/biblioteca/acervo/domain/model.py (antes — commit ecce5f6)
class Livro:
    def __init__(self, isbn: str, titulo: str, autor: str):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.exemplares: List[Exemplar] = []
        self.ativo = True

    def adicionar_exemplar(self, exemplar: Exemplar):
        self.exemplares.append(exemplar)

    def inativar(self):
        for exemplar in self.exemplares:
            if exemplar.status == "emprestado":
                raise Exception(f"O livro '{self.titulo}' não pode ser inativado pois possui alguns livros emprestados.")
        self.ativo = False
```

### Problema concreto

A lógica de validação estava misturada diretamente com a mudança de estado dentro do método `inativar()`. Com isso:

1. Não era possível apenas consultar se um livro estava elegível para inativação sem executar a mutação `self.ativo = False` (violação de SRP).
2. Se no futuro a regra de inativação precisasse considerar critérios adicionais (como exemplares em manutenção ou histórico), seria necessário modificar diretamente o método que altera o estado da entidade (OCP).
3. No adaptador ORM (`src/biblioteca/acervo/adapters/orm.py`), chamadas repetidas a `start_mappers()` entre suítes de teste causavam erro de remapeamento por falta de `clear_mappers()` e de guarda de idempotência.

### Refatoração

Commits "depois" (do próprio autor): `af2da29`, `dc0ac0f`, `54ce4dc` e `2fc2eea`.

Arquivos envolvidos:
- `src/biblioteca/acervo/domain/model.py`: o comportamento foi separado em três etapas com responsabilidades bem definidas:
  - `pode_ser_inativado()` responde se a operação é permitida;
  - `validar_inativacao()` dispara a exceção quando a regra é violada;
  - `inativar()` executa a transição de estado após validar.
- `src/biblioteca/acervo/service_layer/services.py`: orquestra `adicionar_livro`, `listar_livros` e `inativar_livro` dependendo de `AbstractRepository` (DIP).
- `src/biblioteca/acervo/adapters/orm.py`: adiciona `clear_mappers()` e verificação de `_sa_class_manager` em `start_mappers()`.
- `src/biblioteca/acervo/tests/unit/test_services_acervo.py` (novo): testes unitários da camada de serviço com `FakeRepository` e `DummySession`.

```python
# src/biblioteca/acervo/domain/model.py (depois — commits af2da29 e dc0ac0f)
    def pode_ser_inativado(self) -> bool:
        return not any(exemplar.status == "emprestado" for exemplar in self.exemplares)

    def validar_inativacao(self):
        if not self.pode_ser_inativado():
            raise Exception(
                f"O livro '{self.titulo}' não pode ser inativado pois possui alguns livros emprestados."
            )

    def inativar(self):
        self.validar_inativacao()
        self.ativo = False
```

### Como os testes garantiram o comportamento

- Os testes da Fase 1 (`src/biblioteca/acervo/tests/unit/test_acervo.py`, `tests/integration/test_repository.py` e `tests/e2e/test_api.py`) continuaram passando sem alteração, garantindo que o comportamento observável do domínio, do repositório SQLite e da API Flask foi preservado.
- Foram adicionados 3 novos testes unitários em `src/biblioteca/acervo/tests/unit/test_services_acervo.py` (`test_adicionar_livro_persiste_livro_no_repositorio`, `test_inativar_livro_altera_estado_do_livro` e `test_inativar_livro_lanca_erro_quando_nao_existe`), validando os casos de uso em memória com `FakeRepository` e `DummySession`.

### Custo da refatoração

- A entidade `Livro` passou a ter três métodos em vez de um para o fluxo de inativação, aumentando levemente a indireção interna, além da criação de `DummySession` nos testes unitários da camada de serviço.
- O custo é pequeno e compensa porque separa consulta, validação e mutação de estado (SRP), facilita a extensão da regra de inativação (OCP) e comprova o desacoplamento da camada de serviço em relação ao SQLAlchemy (DIP).

## João Vicente Piller Menezes — Reserva

### Princípio violado

**Open/Closed Principle (OCP):** a entidade `Reserva` deveria estar aberta para extensão
(novos prazos de retirada) e fechada para modificação. Porém, o prazo de 48 horas estava
fixo dentro do método `esta_expirada`, de modo que qualquer mudança de prazo exigia
alterar a própria classe de domínio.

### Código antes

Introduzido no commit `f185330` (22/09/2026), anterior a 06/10/2026:

```python
# src/biblioteca/reservas/domain/model.py
def esta_expirada(self, data_hora_atual: datetime) -> bool:
    if self.status == "Disponivel" and self.data_disponibilizacao is not None:
        return (data_hora_atual - self.data_disponibilizacao) > timedelta(hours=48)
    return False
```

### Problema concreto

Mudança de requisito plausível: a biblioteca passa a dar prazos de retirada diferentes
conforme a categoria do leitor (por exemplo, 72 horas para professores e 48 horas para
alunos), regra que já aparece no agregado de Cadastro de Leitores (`CategoriaLeitor`).

Com o prazo fixo no código, atender esse requisito obrigaria a modificar `Reserva`
toda vez que um novo prazo surgisse, misturando na entidade uma regra que pertence
à configuração de cada reserva. Além disso, o valor `48` não era persistido, então
não havia como uma reserva carregada do banco "lembrar" o prazo com que foi criada.

### Refatoração

Commit "depois": `14d6d57`

- `domain/model.py`: o prazo virou o atributo `prazo_retirada_horas`, recebido no
  construtor, com o valor padrão `PRAZO_RETIRADA_PADRAO_HORAS = 48`. O método
  `esta_expirada` passou a usar esse atributo.
- `adapters/orm.py`: nova coluna `prazo_retirada_horas` na tabela `reservas`, com
  valor padrão 48 no banco, para que reservas já existentes continuem válidas.
- `service_layer/services.py`: `reservar_livro` aceita um `prazo_retirada_horas`
  opcional.
- `entrypoints/flask_app.py`: o endpoint `POST /reservas` aceita o campo opcional
  `prazo_retirada_horas`.

```python
# src/biblioteca/reservas/domain/model.py (depois)
def esta_expirada(self, data_hora_atual: datetime) -> bool:
    if self.status == "Disponivel" and self.data_disponibilizacao is not None:
        return (data_hora_atual - self.data_disponibilizacao) > timedelta(hours=self.prazo_retirada_horas)
    return False
```

Agora um novo prazo é atendido apenas criando a reserva com outro valor, sem
modificar a classe `Reserva`.

### Como os testes garantiram o comportamento

- Os 16 testes existentes do módulo (unitários, de integração e e2e) continuaram
  passando **sem nenhuma alteração**, inclusive `test_reserva_expira_apos_48_horas_disponivel`
  e o e2e `test_happy_path_transfere_reserva_apos_48_horas`. Isso comprova que o
  comportamento padrão de 48 horas foi preservado.
- Foram adicionados 5 testes para o novo requisito: prazo padrão de 48 horas,
  reserva de 72 horas que não expira com 49 horas e expira com 73 horas, serviço
  com prazo personalizado, persistência do prazo no banco e leitura de uma reserva
  inserida sem prazo (que recebe o padrão de 48 horas).

### Custo da refatoração

- Um atributo a mais na entidade, uma coluna a mais na tabela e um parâmetro opcional
  a mais no serviço e na API.
- O valor padrão precisa existir em dois lugares (na constante do domínio e no
  `server_default` do banco). Para evitar divergência, o ORM usa a própria constante
  `PRAZO_RETIRADA_PADRAO_HORAS`.

O custo é pequeno e compensa: o requisito de prazos por categoria passa a ser atendido
sem modificar a entidade, e o comportamento antigo fica intacto por padrão. Quem decide
o prazo de cada leitor ainda não está definido. Essa escolha pode virar um padrão GoF
(por exemplo, Strategy) no checkpoint 3.

## Sandy Fortes Cabral — Empréstimo

### Princípios violados

- **Liskov Substitution Principle (LSP):** `SqlAlchemyRepository` e `FakeRepository`
  implementam o mesmo contrato `AbstractRepository`, mas reagiam de formas diferentes
  quando o item não existia.
- **Dependency Inversion Principle (DIP):** o entrypoint Flask precisava importar
  `NoResultFound`, uma exceção concreta do SQLAlchemy, para traduzir o erro de negócio
  em HTTP 404. A camada de entrada dependia de um detalhe do framework de persistência.

### Código antes

O comportamento abaixo foi introduzido nos meus commits `4202941` (repositório,
23/09/2026) e `719453d` (entrypoint, 28/09/2026), anteriores a 06/10/2026. O snapshot
com os caminhos atuais da estrutura por agregado é o commit `1cd3fa3` (29/09/2026):

```python
# src/biblioteca/emprestimo/adapters/repository.py
class SqlAlchemyRepository(AbstractRepository):
    def get(self, id_item: str) -> model.ItemEmprestado:
        return (
            self.session.query(model.ItemEmprestado)
            .filter_by(id_item=id_item)
            .one()  # levanta sqlalchemy.orm.exc.NoResultFound
        )


class FakeRepository(AbstractRepository):
    def get(self, id_item: str) -> model.ItemEmprestado:
        return next(  # levanta StopIteration
            item for item in self._items
            if item.id_item == id_item
        )
```

```python
# src/biblioteca/emprestimo/entrypoints/flask_app.py
from sqlalchemy.orm.exc import NoResultFound

# ...
        except NoResultFound:
            return jsonify({"erro": "Item não encontrado"}), 404
```

### Problema concreto

As duas implementações do mesmo contrato tinham pós-condições diferentes para o
mesmo caso de uso: buscar um item inexistente. O repositório real lançava
`NoResultFound`, enquanto o fake lançava `StopIteration`. Consequências práticas:

1. Substituir o repositório real pelo fake em um teste de serviço ou de API mudava o
   tipo de exceção e podia produzir HTTP 500 em vez de 404, violando LSP.
2. O `flask_app.py` só tratava `NoResultFound`, então o tratamento de "item não
   encontrado" ficava acoplado ao SQLAlchemy. Uma nova implementação de repositório
   (por exemplo, em memória ou outro banco) exigiria alterar a camada de entrada,
   violando DIP.
3. O contrato `AbstractRepository.get` não documentava o comportamento de ausência,
   deixando a decisão a cargo de cada implementação.

### Refatoração

Commit "depois": `f275b6f` — os arquivos alterados são:

- `src/biblioteca/emprestimo/domain/exceptions.py` (novo): define
  `ItemNaoEncontrado`, uma exceção de domínio que faz parte do contrato do
  repositório.
- `src/biblioteca/emprestimo/adapters/repository.py`: `AbstractRepository.get`
  documenta que deve levantar `ItemNaoEncontrado`; as duas implementações passam a
  levantar essa mesma exceção. O `SqlAlchemyRepository` traduz `NoResultFound` para
  `ItemNaoEncontrado`; o `FakeRepository` levanta a exceção diretamente.
- `src/biblioteca/emprestimo/entrypoints/flask_app.py`: deixa de importar
  `NoResultFound` e passa a capturar `ItemNaoEncontrado`.

```python
# domain/exceptions.py
class ItemNaoEncontrado(Exception):
    def __init__(self, id_item: str):
        self.id_item = id_item
        super().__init__(f"Item de empréstimo {id_item} não encontrado.")


# adapters/repository.py
class SqlAlchemyRepository(AbstractRepository):
    def get(self, id_item: str) -> model.ItemEmprestado:
        try:
            return (
                self.session.query(model.ItemEmprestado)
                .filter_by(id_item=id_item)
                .one()
            )
        except NoResultFound as exc:
            raise ItemNaoEncontrado(id_item) from exc


class FakeRepository(AbstractRepository):
    def get(self, id_item: str) -> model.ItemEmprestado:
        for item in self._items:
            if item.id_item == id_item:
                return item
        raise ItemNaoEncontrado(id_item)
```

### Como os testes garantiram a preservação do comportamento

- Os testes da Fase 1 continuam passando sem alteração: os quatro testes de serviço,
  os testes do fake, os testes de integração e os testes E2E do Empréstimo.
- `test_fake_repository_levanta_item_nao_encontrado` e
  `test_sqlalchemy_repository_levanta_item_nao_encontrado` verificam que as duas
  implementações agora levantam o mesmo `ItemNaoEncontrado` e expõem o `id_item` na
  exceção.
- Os testes E2E existentes confirmam que o endpoint de devolução continua retornando
  HTTP 404 para item inexistente. Foi acrescentado
  `test_api_retorna_404_para_atraso_de_item_inexistente` para cobrir o outro endpoint
  que consulta o repositório.
- Execução local da suíte do Empréstimo: `25 passed` com
  `python -m pytest src/biblioteca/emprestimo/tests -q`. As três etapas da CI
  (unitária, integração e E2E) também passam.

### Custo da refatoração e por que compensa

A refatoração adiciona uma classe de exceção, dois blocos de tradução de erro nos
adapters e uma dependência a mais do adapter para o domínio. Há mais indireção do que
simplesmente deixar cada repositório lançar a exceção nativa.

O custo compensa porque o contrato passa a ser explícito e substituível: qualquer
implementação de repositório agora tem o mesmo comportamento observável, e a camada
HTTP não conhece SQLAlchemy. Isso torna o teste E2E possível com o fake, reduz o
acoplamento do entrypoint e elimina uma causa concreta de 500 em vez de 404.

## Ana Laura Neuhaus Vega — Multas

### Princípios violados

- **Liskov Substitution Principle (LSP):** `SqlAlchemyMultaRepository` e `FakeMultaRepository` implementavam a abstração `AbstractMultaRepository`, mas reagiam de formas diferentes quando uma multa não era encontrada. O repositório real retornava `None` (ou deixava vazar `NoResultFound` do SQLAlchemy), enquanto a verificação de ausência ficava solta.
- **Dependency Inversion Principle (DIP):** o caso de uso na camada de serviço (`pagar_multa`) e a API Flask (`flask_app.py`) dependiam de exceções genéricas (`ValueError`), fazendo com que o tratamento de erro da camada de aplicação e de apresentação dependesse de validações procedurais em vez de exceções de domínio explícitas.

### Código antes

Comportamento introduzido nos commits `2392022` (repositório, 28/09/2026) e `b9de837` (API Flask, 29/09/2026), ambos anteriores a 06/10/2026:

```python
# src/biblioteca/multas/adapters/repository.py (antes)
class SqlAlchemyMultaRepository(AbstractMultaRepository):
    def get(self, id_multa: str) -> model.Multa:
        return self.session.query(model.Multa).filter_by(id_multa=id_multa).first()

# src/biblioteca/multas/service_layer/services.py (antes)
def pagar_multa(id_multa: str, valor: float, data_pgto: date, repo: AbstractMultaRepository, session):
    multa = repo.get(id_multa)
    if multa is None:
        raise ValueError(f"Multa {id_multa} não encontrada.")
    
    multa.registrar_pagamento(model.Pagamento(valor=valor, data=data_pgto))
    session.commit()
```

### Problema concreto

Como a abstração `AbstractMultaRepository.get` não definia uma pós-condição clara para o caso de um objeto ausente, cada repositório lidava com a busca à sua maneira. Isso gerava dois problemas práticos:

1. **Violação de LSP:** Se alterássemos a implementação do repositório no teste ou na API, a forma de sinalizar ausência do registro não era garantida por contrato. A verificação de retorno `None` ficava sob responsabilidade manual da camada de serviço, misturando orquestração com validação de contrato de persistência.
2. **Violação de DIP:** Ao tratar a ausência com `ValueError` genérico, a API Flask não conseguia diferenciar com clareza uma falha de entidade ausente (HTTP 404) de uma falha de parâmetro de requisição malformado (HTTP 400). Além disso, a camada web dependia de condicionais na camada de serviço em vez de tratar exceções puras da camada de domínio.

### Refatoração

Commit "depois": `0452ae0`, `a3fafad`, `6f219b0`, `9be867e`, `a705916`, `1f18f9e` — os arquivos alterados foram:

- `src/biblioteca/multas/domain/exceptions.py` (novo): define `MultaNaoEncontrada` e `ValorPagamentoInvalido`, exceções puras de domínio.
- `src/biblioteca/multas/domain/model.py`: adiciona validação no `__post_init__` do Value Object `Pagamento` para impedir valores zerados ou negativos.
- `src/biblioteca/multas/adapters/repository.py`: `AbstractMultaRepository.get` documenta que deve lançar `MultaNaoEncontrada`. `SqlAlchemyMultaRepository` traduz `NoResultFound` para `MultaNaoEncontrada`, e `FakeMultaRepository` passa a lançar a mesma exceção.
- `src/biblioteca/multas/service_layer/services.py`: simplifica a orquestração removendo o `if multa is None`, confiando na garantia do contrato do repositório.
- `src/biblioteca/multas/entrypoints/flask_app.py`: passa a capturar `MultaNaoEncontrada` (retornando HTTP 404) e `ValorPagamentoInvalido` (retornando HTTP 400).

```python
# src/biblioteca/multas/domain/exceptions.py (depois)
class MultaNaoEncontrada(Exception):
    def __init__(self, id_multa: str):
        self.id_multa = id_multa
        super().__init__(f"Multa {id_multa} não encontrada.")

# src/biblioteca/multas/adapters/repository.py (depois)
class SqlAlchemyMultaRepository(AbstractMultaRepository):
    def get(self, id_multa: str) -> model.Multa:
        try:
            return self.session.query(model.Multa).filter_by(id_multa=id_multa).one()
        except NoResultFound as exc:
            raise MultaNaoEncontrada(id_multa) from exc

class FakeMultaRepository(AbstractMultaRepository):
    def get(self, id_multa: str) -> model.Multa:
        for m in self._multas:
            if m.id_multa == id_multa:
                return m
        raise MultaNaoEncontrada(id_multa)
```

### Como os testes garantiram o comportamento

- **Preservação da suíte existente:** Os testes da Fase 1 (`test_multas.py`, `test_services.py` e `test_multas_api.py`) continuaram passando sem quebras.
- **Novos testes unitários:** Foram adicionados testes em `test_multas.py` para garantir que instanciar um `Pagamento` com valor menor ou igual a zero dispara `ValorPagamentoInvalido`.
- **Validação de contrato dos repositórios:** Foi adicionado teste unitário garantindo que tanto `SqlAlchemyMultaRepository` quanto `FakeMultaRepository` disparam exatamente a exceção `MultaNaoEncontrada` quando consultados por um ID inexistente.
- **Teste E2E de contrato HTTP:** O teste da API confirmou que requisições de pagamento para multas inexistentes retornam status `404 Not Found` de maneira consistente.

### Custo da refatoração

- Adição de um arquivo de exceções (`domain/exceptions.py`) e blocos `try/except` de tradução nos adapters de repositório e no entrypoint Flask.
- Há um nível a mais de indireção ao transformar exceções do banco em exceções de domínio.

O custo compensa porque unifica o contrato entre os repositórios real e *fake* (atendendo ao LSP), desacopla a API Flask de erros genéricos ou de infraestrutura (atendendo ao DIP) e torna as respostas da API previsíveis e alinhadas ao padrão de erros adotado pelos demais agregados da biblioteca.

## Karine Vitória Marinho de Moraes — Manutenção e Conservação do Acervo

### Princípio violado

- **Single Responsibility Principle (SRP):** A classe `OrdemServico` possuía a responsabilidade de validar tanto as condições do laudo de avaliação quanto a disponibilidade do exemplar para manutenção. Entretanto, a disponibilidade é uma informação relacionada ao agregado Acervo, enquanto a validação da reparabilidade pertence ao contexto de Manutenção.

### Código antes

Comportamento presente no commit `4da1b30` (29/09/2026), anterior a 06/10/2026:

```python
# src/biblioteca/manutencao/domain/model.py

class OrdemServico:
    def __init__(
        self,
        id_ordem: str,
        laudo: LaudoAvaliacao,
        exemplar_disponivel: bool
    ):
        if not exemplar_disponivel:
            raise ValueError(
                "Não é possível criar uma ordem de serviço sem um exemplar disponível."
            )

        if not laudo.reparavel:
            raise ValueError(
                "Não é possível criar uma ordem de serviço para um dano não reparável."
            )

        self.id_ordem = id_ordem
        self.laudo = laudo
        self.status = OrdemServicoStatus.ABERTA
```

### Problema concreto

A entidade `OrdemServico` concentrava validações relacionadas a duas responsabilidades distintas: as condições necessárias para a manutenção e a disponibilidade do exemplar no Acervo.

Isso gerava acoplamento entre os agregados, pois uma mudança nas regras de disponibilidade do Acervo poderia exigir alterações na entidade `OrdemServico`, mesmo que as regras próprias da manutenção permanecessem iguais.

### Refatoração

Commit "depois": `5e0d902`.

A refatoração consistiu em transferir a validação da disponibilidade do exemplar para a camada `service_layer`, mantendo na entidade `OrdemServico` apenas a validação relacionada à reparabilidade do dano.

No arquivo `src/biblioteca/manutencao/domain/model.py`, o construtor passou a receber apenas o identificador da ordem e o laudo:

```python
class OrdemServico:
    def __init__(
        self,
        id_ordem: str,
        laudo: LaudoAvaliacao
    ):
        if not laudo.reparavel:
            raise ValueError(
                "Não é possível criar uma ordem de serviço para um dano não reparável."
            )

        self.id_ordem = id_ordem
        self.laudo = laudo
        self.status = OrdemServicoStatus.ABERTA
```

No arquivo `src/biblioteca/manutencao/service_layer/services.py`, a verificação de disponibilidade passou a acontecer antes da criação da entidade:

```python
def criar_ordem_servico(
    self,
    id_ordem: str,
    laudo: model.LaudoAvaliacao,
    exemplar_disponivel: bool
) -> model.OrdemServico:

    if not exemplar_disponivel:
        raise ValueError(
            "Não é possível criar uma ordem de serviço sem um exemplar disponível."
        )

    ordem_servico = model.OrdemServico(
        id_ordem=id_ordem,
        laudo=laudo
    )

    self.repository.add(ordem_servico)

    return ordem_servico
```

### Como os testes garantiram o comportamento

Após a refatoração, foram executados os testes do agregado de Manutenção, totalizando 10 testes aprovados em 0,10 segundos.

- **Testes unitários:** verificaram a criação de ordens de serviço e a rejeição de laudos associados a danos não reparáveis.
- **Testes de integração:** verificaram a persistência, recuperação e listagem das ordens de serviço e seus respectivos laudos.
- **Testes E2E:** verificaram o funcionamento dos serviços e da API após a alteração.

A aprovação de toda a suíte demonstrou que a refatoração não provocou regressões nos comportamentos já existentes.

### Custo da refatoração

A alteração exigiu modificar a assinatura do construtor de `OrdemServico` e atualizar os pontos do código que criavam essa entidade. A validação de disponibilidade passou a ser responsabilidade da camada de serviço, que agora concentra essa verificação antes de solicitar a criação da ordem.

O custo da mudança foi pequeno, pois não exigiu a criação de novas classes ou estruturas. A alteração compensa por separar as responsabilidades dos agregados e reduzir o acoplamento entre Manutenção e Acervo.

## Isabella Vieira da Motta — Leitores

### Princípios violados

- **Single Responsibility Principle (SRP):** A entidade raiz `Leitor` acumulava a gestão dos seus dados cadastrais e o processamento de regras mutáveis, como a lógica de limites de empréstimo por categoria.
- **Open/Closed Principle (OCP):** O método `inativar()` era rígido. Adicionar novos efeitos colaterais (como enviar emails ou cancelar reservas pendentes) exigiria modificar a classe principal, violando a premissa de que deve estar fechada para modificação e aberta para extensão.

### Código antes

Comportamento introduzido nos primeiros commits do agregado (final de setembro de 2026):

```python
# src/biblioteca/cadastro/domain/model.py (antes)
class Leitor:
    def __init__(self, nome: str, email: str, tipo_categoria: str, emprestimos_ativos: int = 0):
        self.nome = nome
        self.tipo_categoria = tipo_categoria
        self.emprestimos_ativos = emprestimos_ativos
        self.ativo = True

    def pode_fazer_emprestimo(self) -> bool:
        if not self.ativo:
            return False
        limite = 3 if self.tipo_categoria == "Aluno" else 5
        return self.emprestimos_ativos < limite
        
    def inativar(self):
        self.ativo = False
```

### Problema concreto

Como a entidade `Leitor` concentrava as regras de negócio e as ações de mudança de estado, surgiram dois problemas:

1. **Violação de SRP:** Mudanças na política da biblioteca (ex: alterar limites) exigiam alterar e retestar toda a entidade `Leitor`.
2. **Violação de OCP:** A necessidade de engatilhar eventos externos durante a inativação forçaria a entidade a conhecer serviços de fora, criando um forte acoplamento no domínio.

### Refatoração

A separação (VO) ocorreu na Fase 1 e a extensão (Observer) na Fase 2. Os arquivos alterados foram:

- `src/biblioteca/cadastro/domain/model.py`: Criação do VO `CategoriaLeitor` (SRP) e da interface `LeitorObserver` (OCP).
- `src/biblioteca/cadastro/adapters/orm.py`: Uso do padrão *Composite* do SQLAlchemy para o VO.
- `src/biblioteca/cadastro/tests/unit/test_leitor_observer.py` (novo): Testes da notificação.

```python
# src/biblioteca/cadastro/domain/model.py (depois)
import abc

class CategoriaLeitor:
    def __init__(self, nome: str, limite_emprestimos: int):
        self.nome = nome
        self.limite_emprestimos = limite_emprestimos

class LeitorObserver(abc.ABC):
    @abc.abstractmethod
    def leitor_inativado(self, leitor):
        pass

class Leitor:
    def __init__(self, nome: str, email: str, categoria: CategoriaLeitor):
        self.nome = nome
        self.categoria = categoria  # Limite delegado ao VO (SRP)
        self.ativo = True

    @property
    def observers(self):
        if not hasattr(self, '_observers'):
            self._observers = []
        return self._observers

    def adicionar_observer(self, observer: LeitorObserver):
        self.observers.append(observer)

    def inativar(self):
        self.ativo = False
        for obs in self.observers:
            obs.leitor_inativado(self) # Aberto para extensão (OCP)
```

### Como os testes garantiram o comportamento
- **Preservação da suíte existente:** Os testes E2E e de repositório continuaram passando, validando o mapeamento ORM sem quebrar com a nova lista de observadores.
- **Novos testes unitários de OCP:** O `MockEmailObserver` em `test_leitor_observer.py` validou a alteração de estado externo após a notificação de inativação.
- **Validação de SRP:** Testes unitários focados na `CategoriaLeitor` garantiram a checagem isolada de limites.

### Custo da refatoração

- Exigiu o uso do decorador `@property` para instanciar a lista de observers dinamicamente, impedindo erros no mapeamento do SQLAlchemy.
- Maior complexidade no ORM devido ao uso do *Composite* para achatar o VO `CategoriaLeitor`.

O custo compensa porque blinda o núcleo do usuário contra mudanças em regras de empréstimo (SRP) e permite reagir à inativação integrando múltiplos serviços externos de forma limpa, sem modificar o domínio (OCP).