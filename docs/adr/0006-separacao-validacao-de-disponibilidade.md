# ADR 0006 — Separaração da validação de disponibilidade do exemplar

- **Status:** Aceita
- **Autora:** Karine Vitória Marinho de Moraes

## Contexto

A entidade `OrdemServico` representa uma ordem de serviço associada a um laudo de avaliação. Inicialmente, seu construtor verificava tanto se o dano era reparável quanto se havia um exemplar disponível.

Entretanto, a disponibilidade do exemplar está relacionada ao módulo de Acervo, enquanto a reparabilidade pertence ao domínio de Manutenção. Essa divisão de responsabilidades motivou a refatoração.

## Decisão
Transferir a validação de disponibilidade do exemplar para a camada de serviço, mantendo na entidade `OrdemServico` apenas a validação relacionada à reparabilidade do dano.

Assim, o construtor passa a receber somente o identificador da ordem e o laudo de avaliação. A validação de disponibilidade é realizada pelo método `criar_ordem_servico`, da classe `OrdemServicoService`, antes da instanciação da entidade.

Dessa forma, a entidade permanece responsável por garantir que somente danos reparáveis possam gerar ordens de serviço, enquanto o serviço verifica a disponibilidade necessária para a criação.

## Alternativas consideradas

1. **Manter as duas validações no construtor de `OrdemServico`:**
seria uma implementação simples, mas manteria na entidade uma responsabilidade relacionada ao controle do Acervo, aumentando o acoplamento entre os módulos.
2. **Remover a validação de disponibilidade:**
simplificaria a criação da entidade, mas permitiria a abertura de ordens de serviço sem a disponibilidade necessária para sua realização.
3. **Transferir a validação para a camada de serviço (escolhida):**
mantém a regra de reparabilidade na entidade e desloca a verificação de disponibilidade para o serviço, separando as responsabilidades.

## Consequências

### Positivas

- A entidade `OrdemServico` passa a concentrar somente as validações relacionadas ao seu próprio domínio.
- Redução do acoplamento entre Manutenção e Acervo.
- Separação mais clara das responsabilidades entre entidade e camada de serviço.
- As validações podem ser testadas de forma independente.

### Negativas

- A camada de serviço passa a concentrar também a verificação de disponibilidade do exemplar.

## Evidências

- `4da1b30`: registra a implementação inicial de OrdemServico, na qual o construtor recebia a informação de disponibilidade do exemplar.
- `5e0d902`: registra a refatoração que transferiu essa validação para OrdemServicoService, mantendo na entidade somente a verificação de reparabilidade do dano.
- `7e24828`: documenta a refatoração realizada com base no princípio da Responsabilidade Única (SRP).