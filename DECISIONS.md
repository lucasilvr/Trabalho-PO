# DECISIONS

## Karine Vitória Marinho de Moraes

### Fase 1 - Checkpoint 1

#### Implementação

23-09-2026 
`505aceb` — feat: criar entidades
Realizei a implementação do agregado, sendo composto pelas entidades "OrdemServico", que representa a solicitação de manutenção, e "LaudoAvaliacao", que registra as infromações relacionadas ao dano no exemplar, além do "OrdemServicoStatus", responsável por padronizar os estados possíveis de uma ordem de serviço.

25-09-2026 
`a66c65` — feat: implementar comportamento nas entidades
Foquei na validação das condições necessárias para a criação e execução da reparação de dano no exemplar.

#### Arquivos

- `src/biblioteca/domain/model.py`

- `tests/unit/test_manutencao.py`

#### Testes

25-09-2026 
`2200aac` — feat: adicionar testes unitários
Os testes unitários verificam as principais regras de criação do agregado: 
- O primeiro teste valida a criação de uma OrdemServico com dados válidos com o status "ABERTA".
- O segundo teste verifica a regra de negócio que impede a criação de uma OrdemServico quando o dano não é reparável.

#### Decisão de projeto

23-09-2026 
A utilização do Enum teve como objetivo representar possíveis status da OrdemServico com valores padronizados.
