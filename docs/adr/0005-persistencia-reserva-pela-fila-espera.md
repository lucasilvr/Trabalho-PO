# ADR 0005 — Persistir a Reserva apenas pela FilaEspera

- **Status:** Aceita
- **Autor:** João Vicente Piller Menezes
- **Data:** 13/11/2026 (registra uma decisão tomada na Fase 1, em 29/09/2026)

## Contexto

O agregado de Reserva tem duas entidades: `FilaEspera`, que representa a fila de leitores
esperando um livro, e `Reserva`, que representa o pedido de um leitor dentro dessa fila.
A principal invariante do agregado envolve as duas ao mesmo tempo: quando um exemplar é
devolvido, o primeiro leitor pendente recebe o direito de retirada e, se não retirar o
livro dentro do prazo, o direito passa para o próximo da fila.

Na Fase 1, ao implementar o Repository Pattern (commit `75a7802`), foi preciso decidir se
cada entidade teria o seu próprio repositório ou se a persistência passaria por uma única
entrada.

## Decisão

Tratar `FilaEspera` como raiz do agregado e persistir as reservas exclusivamente através
dela. Existe apenas o `AbstractFilaEsperaRepository`, com as implementações
`SqlAlchemyFilaEsperaRepository` e `FakeFilaEsperaRepository`
(`src/biblioteca/reservas/adapters/repository.py`). As reservas são carregadas e salvas
junto com a fila pelo relacionamento `reservas` do mapeamento ORM
(`src/biblioteca/reservas/adapters/orm.py`), ordenadas por `data_reserva`.

## Alternativas consideradas

1. **Um repositório para cada entidade (`ReservaRepository` e `FilaEsperaRepository`):**
   permitiria buscar e alterar uma reserva diretamente, mas qualquer caso de uso poderia
   expirar ou disponibilizar uma reserva sem passar pela fila, contornando a regra de
   transferência do direito.
2. **Somente um `ReservaRepository`, montando a fila por consulta:** a fila deixaria de
   existir como objeto do domínio e a regra de ordem e transferência ficaria espalhada
   nos serviços.
3. **Repositório apenas da raiz `FilaEspera` (escolhida):** toda alteração em uma reserva
   passa pela fila, que é quem conhece a ordem dos leitores e aplica a invariante.

## Consequências

### Positivas

- A invariante de transferência do direito fica em um único lugar (`FilaEspera`).
- Os serviços (`reservar_livro`, `registrar_devolucao`, `atualizar_fila`) sempre carregam
  a fila inteira, então não conseguem alterar uma reserva fora de contexto.
- Só há um contrato de repositório, um fake e uma implementação real para manter.

### Negativas

- Para consultar uma única reserva é preciso carregar a fila do livro inteira.
- Não existe uma consulta direta do tipo "todas as reservas de um leitor"; ela exigiria
  um novo método ou percorrer várias filas.
- Filas muito longas aumentariam o custo de cada operação, já que todas as reservas
  são carregadas junto com a fila.

## Evidências

- `75a7802` adicionou o repositório de `FilaEspera` sem repositório próprio para `Reserva`.
- `2496e8f` adicionou o mapeamento ORM com o relacionamento `reservas` da fila.
- `00a795e` (Fase 2) aplicou o padrão State na `Reserva` sem precisar mudar o repositório,
  já que os estados continuam sendo salvos pela `FilaEspera`.
