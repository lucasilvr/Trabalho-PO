## Refatorações SOLID

### Isabella Vieira da Motta - Princípio da Responsabilidade Única (SRP) e Aberto/Fechado (OCP)
* **Agregado:** Leitores
* **Princípio Violado:** SRP e OCP na camada de serviço.
* **O Problema:** A função `cadastrar_leitor` (no commit anterior `332e5ce`) definia internamente o dicionário de limites (`{"Aluno": 3, "Professor": 5}`). Isso forçava a camada de serviço (que deve apenas orquestrar) a conhecer regras de negócio profundas. Qualquer nova categoria exigiria modificar o orquestrador.
* **A Refatoração (Commit `afd8594`):** Criei a classe `FabricaCategoriaLeitor` dentro de `model.py` (Domínio) para centralizar as regras de criação. O serviço agora apenas tenta instanciar e captura o erro, delegando a responsabilidade de conhecimento dos limites para o domínio puro.
* **Testes e Custo:** A suíte de testes unitários e E2E confirmou que o comportamento original foi preservado. O custo foi a adição de uma nova classe Fábrica e uma indireção leve, o que compensa totalmente pela blindagem do serviço contra mudanças de regras de negócio.