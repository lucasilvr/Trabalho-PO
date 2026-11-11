# SOLID no agregado de Acervo

## Contexto

O agregado de Acervo representa o catálogo da biblioteca e centraliza a regra mais importante do módulo: um livro só pode ser inativado quando todos os seus exemplares estiverem disponíveis.

A refatoração aplicada no agregado busca manter essa regra explícita no domínio, deixando a camada de serviço responsável apenas por orquestrar a operação e validar entradas simples.

## Princípios SOLID aplicados

### 1. SRP (Single Responsibility Principle)

A entidade `Livro` continua sendo responsável por seu estado e por suas validações internas, mas a regra de negócio ficou melhor distribuída:

- `pode_ser_inativado()` responde se a operação é permitida
- `validar_inativacao()` dispara a exceção quando a regra é violada
- `inativar()` executa apenas a transição de estado

Antes, a validação e a mutação ficaram concentradas em um único método. Agora, o comportamento ficou mais legível e mais fácil de evoluir.

### 2. OCP (Open/Closed Principle)

A regra de inativação foi organizada como um ponto de extensão do comportamento do agregado, sem exigir mudanças invasivas no restante do sistema.

Se no futuro a regra passar a considerar dados adicionais, como categoria de leitor, histórico de exemplares ou regras de manutenção, esse ajuste pode ser feito sem quebrar o contrato do módulo.

### 3. DIP (Dependency Inversion Principle)

A camada de serviço continua dependendo de abstrações, e não de detalhes da infraestrutura. Ela trabalha com `AbstractRepository`, e não com a implementação concreta do banco.

Isso permite testar o caso de uso com um repositório em memória, sem depender do SQLAlchemy diretamente.

## Antes e depois

### Antes

A lógica de validação estava executada diretamente dentro do método `inativar()`. Esse design funciona, mas mistura responsabilidade de validação e de mudança de estado em um único ponto.

### Depois

A sequência foi separada em três etapas bem definidas:

1. verificar se o livro pode ser inativado
2. validar a regra de domínio
3. alterar o estado do objeto

Essa estrutura reduz acoplamento, melhora a legibilidade e facilita novos testes.

## Arquivos envolvidos

- `src/biblioteca/acervo/domain/model.py`
- `src/biblioteca/acervo/service_layer/services.py`
- `src/biblioteca/acervo/adapters/orm.py`
- `src/biblioteca/acervo/tests/unit/test_services_acervo.py`

## Conclusão

A refatoração do agregado Acervo melhora a clareza do domínio e centraliza a regra de negócio principal em um ponto mais explícito. Isso torna o módulo mais fácil de testar, mais fácil de manter e mais aderente aos princípios SOLID.
# Refatorações SOLID — Fase 2

Este documento registra as violações de SOLID encontradas no código da Fase 1 e as
refatorações feitas na Fase 2. Cada integrante documenta a sua própria refatoração,
no agregado ou módulo sob sua responsabilidade. O grupo deve cobrir, somadas as
seções, pelo menos três princípios diferentes.

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