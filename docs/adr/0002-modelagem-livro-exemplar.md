# ADR 0002 — Representar livro e exemplar separadamente no Acervo

- **Status:** Aceita
- **Autor:** Lucas Dias Silveira
- **Data:** 22/10/2026

## Contexto

No domínio Biblioteca, um livro representa uma obra/catalogação, enquanto um exemplar representa uma unidade física que pode ser emprestada, devolvida ou sofrer manutenção. Tratar esses conceitos como um único objeto dificultaria representar vários exemplares de uma mesma obra e acompanhar a situação individual de cada unidade.

## Decisão

Manter Livro e Exemplar como conceitos distintos no módulo de Acervo, relacionando cada exemplar à obra correspondente. As operações sobre a obra e as operações sobre uma unidade física devem usar o conceito apropriado, respeitando as regras do domínio existentes no código.

## Alternativas consideradas

1. **Uma única entidade para obra e exemplar:** simplifica o modelo inicial, mas complica obras com várias cópias e o controle da disponibilidade individual.
2. **Livro e Exemplar separados (escolhida):** representa cada nível do domínio, mas exige relacionamento entre objetos e cuidados adicionais na persistência e nas consultas.
3. **Usar apenas um catálogo externo como fonte dos exemplares:** poderia ajudar na catalogação, mas não substituiria o controle local de disponibilidade, empréstimos e manutenção.

## Consequências

### Positivas

- Permite que uma obra tenha múltiplos exemplares.
- A disponibilidade e o estado físico são controlados por unidade.
- Regras como impedir inativação quando há exemplar emprestado podem considerar os relacionamentos corretos.

### Negativas

- Consultas do acervo podem precisar combinar Livro e Exemplar.
- Mapeamento ORM, repositórios e testes precisam preservar o relacionamento entre os conceitos.

## Evidências

- O módulo de Acervo tem histórico de implementação da estrutura de Livro e de seu método de inativação; Lucas deve confirmar os hashes e os nomes das classes no histórico atual antes de finalizar esta seção.
- A proposta da Biblioteca prevê controle de exemplares e restrições relacionadas a empréstimos.
