## Padrões GoF

### Isabella Vieira da Motta - Padrão State (Comportamental)
* **Agregado:** Leitores
* **Contexto e Problema:** A entidade `Leitor` possuía uma variável booleana `ativo`. O método `pode_fazer_emprestimo()` usava condicionais para barrar o fluxo se o leitor estivesse inativo. Conforme novos status surgissem, esse método se tornaria um aninhamento complexo de IFs.
* **Alternativa Considerada:** Pensei em usar *Strategy*, mas como a mudança de permissão está estritamente ligada ao ciclo de vida e estado interno da entidade (ativo/inativo), o *State* é semanticamente mais adequado.
* **Participantes:**
  * **Context:** `Leitor`
  * **State:** `EstadoLeitor` (Classe abstrata)
  * **Concrete States:** `LeitorAtivo`, `LeitorInativo`
* **Custo/Benefício:** O custo foi o aumento do número de classes no domínio e a necessidade de passar a própria instância do leitor (`self`) para o estado. O benefício é a eliminação de ramificações condicionais, facilitando a adição de novos estados futuros.
* **Testes:** Exercitado no arquivo `test_leitor_state.py`.

* **Diagrama de Classes:**
```mermaid
classDiagram
    class Leitor {
        -EstadoLeitor _estado
        +pode_fazer_emprestimo() bool
        +inativar()
    }
    class EstadoLeitor {
        <<abstract>>
        +pode_fazer_emprestimo(leitor) bool
    }
    class LeitorAtivo {
        +pode_fazer_emprestimo(leitor) bool
    }
    class LeitorInativo {
        +pode_fazer_emprestimo(leitor) bool
    }
    Leitor --> EstadoLeitor
    EstadoLeitor <|-- LeitorAtivo
    EstadoLeitor <|-- LeitorInativo