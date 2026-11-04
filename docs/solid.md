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
