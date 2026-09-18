# Proposta de Domínio: Sistema de Gestão de Biblioteca

## 1. Equipe
* **Lucas Dias Silveira** (GitHub: `@lucasilvr`)
* **Sandy Fortes Cabral** (GitHub: `@SandyCabral`)
* **João Vicente Piller Menezes** (GitHub: `@joaopiller`)
* **Isabella Vieira da Motta** (GitHub: `@isabellamott4`)
* **Ana Laura Neuhaus Vega** (GitHub: `@ananeuhausv`)
* **Karine Vitoria Marinho de Moraes** (GitHub: `@kvmoraes`)

## 2. Domínio Escolhido
O domínio consiste em um Sistema de Gestão de Biblioteca responsável por orquestrar o catálogo de livros, as regras de empréstimo, filas de reserva, categorização de leitores, penalidades e multas por atraso. 

## 3. Agregados, Entidades e Divisão de Responsabilidades
O sistema é composto por 5 agregados e 10 entidades de negócio distribuídos da seguinte forma:

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

### Agregado 6: Manutenção e Restauro
* **Responsável:** Karine Vitoria Marinho de Moraes
* **Entidades:** OrdemServico (Raiz de Agregado) e LaudoAvaliacao.
* **Invariante de Domínio:** Uma OrdemServico de restauro só pode ser iniciada se o LaudoAvaliacao indicar que o dano é "reparável" e o exemplar não estiver atualmente "emprestado" a um leitor.
