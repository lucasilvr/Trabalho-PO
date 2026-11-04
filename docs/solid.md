# Refatorações SOLID — Fase 2

Este documento registra as violações de SOLID encontradas no código da Fase 1 e as
refatorações feitas na Fase 2. Cada integrante documenta a sua própria refatoração,
no agregado ou módulo sob sua responsabilidade. O grupo deve cobrir, somadas as
seções, pelo menos três princípios diferentes.

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
