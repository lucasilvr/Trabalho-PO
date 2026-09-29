# Proposta de Domínio: Sistema de Gestão de Biblioteca

## 1. Equipe
* **Lucas Dias Silveira** (GitHub: `@lucasilvr`)
* **Sandy Fortes Cabral** (GitHub: `@SandyCabral`)
* **João Vicente Piller Menezes** (GitHub: `@joaopiller`)
* **Isabella Vieira da Motta** (GitHub: `@isabellamott4`)
* **Ana Laura Neuhaus Vega** (GitHub: `@ananeuhausv`)
* **Karine Vitoria Marinho de Moraes** (GitHub: `@kvmoraes`)

## 2. Domínio Escolhido
O domínio consiste em um Sistema de Gestão de Biblioteca,  responsável por gerenciar o catálogo de livros, as regras de empréstimo, filas de reserva, categorização de leitores, penalidades e multas por atraso e o acompanhamento da manutenção e conservação dos exemplares danificados.

## 3. Agregados, Entidades e Divisão de Responsabilidades
O sistema é composto por 6 agregados e 12 entidades de negócio distribuídos da seguinte forma:

### Agregado 1: Acervo (Catálogo)
* **Responsável:** Lucas Dias Silveira
* **Entidades:** Livro (Raiz de Agregado) e Exemplar.
* **Invariante de Domínio:** Um Livro não pode ser inativado ou excluído do sistema se houver algum exemplar dele com status atual de "emprestado".

### Agregado 2: Empréstimo
* **Responsável:** Sandy Fortes Cabral
* **Entidades:** RegistroEmprestimo (Raiz de Agregado) e ItemEmprestado.
* **Invariante de Domínio:** Um novo empréstimo é bloqueado se o usuário possuir qualquer devolução constando como "em atraso" no sistema.

### Agregado 3: Reserva
* **Responsável:** João Vicente Piller Menezes
* **Entidades:** Reserva (Raiz de Agregado) e FilaEspera.
* **Invariante de Domínio:** Quando um exemplar é devolvido, o direito de reserva expira automaticamente após 48 horas se o primeiro leitor da fila não retirá-lo, transferindo o direito para o próximo da FilaEspera.

### Agregado 4: Cadastro de Leitores
* **Responsável:** Isabella Vieira da Motta
* **Entidades:** Leitor (Raiz de Agregado) e CategoriaLeitor.
* **Invariante de Domínio:** O limite máximo de exemplares emprestados simultaneamente é controlado pelas regras definidas na CategoriaLeitor correspondente ao leitor (ex: limite de alunos vs. professores).

### Agregado 5: Penalidades e Multas
* **Responsável:** Ana Laura Neuhaus Vega
* **Entidades:** Multa (Raiz de Agregado) e Pagamento.
* **Invariante de Domínio:** Uma Multa só altera seu status para "Quitada" se o valor do Pagamento processado for exatamente igual ou superior à taxa calculada automaticamente pelos dias de atraso.

# Informações adicionais

### Agregado 1: Acervo (Livro e Exemplar)
* **Responsável:** Lucas Dias Silveira
**Decisões Arquiteturais e de Design:**
* **Modelagem de Domínio:** Escolhi estruturar `Livro` como a Raiz de Agregado e `Exemplar` como entidade interna subordinada. Isso garante que a regra de negócio central (a inativação do livro) valide todos os status dos exemplares em um único ponto de consistência.
* **ORM Imperativo (Clássico):** A separação estrutural das tabelas no SQLAlchemy (em `orm.py`) permitiu manter as classes do domínio completamente puras, sem herdar dependências de infraestrutura, o que agilizou a execução dos testes unitários.
* **Injeção de Dependência e Repository Pattern:** O uso da interface `AbstractRepository` na camada de serviço facilitou a criação e injeção do `FakeRepository`. Isso desacoplou as regras de negócio do banco de dados e permitiu validar a persistência em memória de forma isolada e performática.

### Agregado 6: Manutenção e Conservação do Acervo
* **Responsável:** Karine Vitoria Marinho de Moraes
* **Entidades:** OrdemServico (Raiz de Agregado) e LaudoAvaliacao.
* **Invariante de Domínio:** Uma OrdemServico de restauração só pode ser iniciada para um exemplar que esteja disponível para manutenção e cujo LaudoAvaliacao indique que o dano é reparável. Um exemplar que esteja "emprestado" não pode ser encaminhado para manutenção.
