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
