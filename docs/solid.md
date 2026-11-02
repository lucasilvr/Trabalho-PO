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
