João Vicente Piller Menezes
Fase 1 — Checkpoint 1
Implementação
22 - 09 - 2026 — feat: implementa entidade Reserva e limite de 48 horas
Implementei o agregado Reserva e estabeleci as lógicas iniciais de verificação de prazo.
23 - 09 - 2026 — feat: implementa agregado FilaEspera com transferencia de direito
Implementei a entidade raiz FilaEspera, encarregada de gerenciar a fila e garantir a transferência de exemplares devolvidos para o próximo da fila, respeitando a invariante de 48 horas estipulada na proposta.
Testes
22 - 09 - 2026 Testes unitários cobrindo transições de estados de uma reserva (Pendente, Disponível e Expirada).
23 - 09 - 2026 Teste unitário protegendo a invariante principal do domínio em atualizar_fila().
Decisão de projeto
22 - 09 - 2026 A verificação `esta_expirada` recebe `data_hora_atual` como injeção de dependência via parâmetro de método, viabilizando o mock da passagem do tempo durante a bateria de testes unitários.

Fase 1 — Checkpoint 2
Implementação
28 - 09 - 2026 — feat: adiciona mapeamento ORM para reserva e fila de espera
29 - 09 - 2026 — feat: implementa repository pattern para a fila de espera
Abstração do acesso a banco via Repository, conforme o livro-texto, mantendo total ausência de dependências de infraestrutura na modelagem inicial.
Testes
29 - 09 - 2026 Implementação do teste de integração com SQLite instanciado em memória, garantindo persistência em cascata da lista de reservas aninhadas a uma fila.
Decisão de projeto
29 - 09 - 2026 Optei por não criar um repositório isolado para a `Reserva`. Sendo ela um objeto interno do agregado, suas persistências deverão ser lidadas exclusivamente através da entidade raiz `FilaEspera`, preservando a consistência arquitetural.