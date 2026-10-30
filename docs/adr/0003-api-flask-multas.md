# ADR 0003 — Separar a API Flask dos casos de uso de Penalidades

- **Status:** Aceita 
- **Autora:** Ana Laura Neuhaus Vega

## Contexto

O módulo de Penalidades/Multas disponibiliza operações HTTP usando Flask e precisa aplicar regras do domínio, como calcular a multa e determinar quando um pagamento permite marcá-la como quitada. A API também precisa transformar requisições e resultados em formatos HTTP/JSON.

Concentrar protocolo HTTP, regras de multa e persistência diretamente nas rotas reduziria a quantidade inicial de arquivos, mas misturaria responsabilidades e dificultaria testar as regras independentemente da API.

## Decisão

Manter a API Flask responsável pelo contrato HTTP — receber requisições, validar o formato de entrada e construir respostas — e delegar os casos de uso à camada de serviço e as regras de negócio às classes de domínio correspondentes. A persistência deve ocorrer por meio do repositório usado pelo módulo.

## Alternativas consideradas

1. **Regras e persistência nas rotas Flask:** menos indireção inicial, mas mistura HTTP, negócio e banco.
2. **Separar entrypoint, serviço e domínio (escolhida):** facilita testes unitários e E2E por camadas, mas exige coordenar rotas, serviços, serialização e tratamento de erros.
3. **Usar outro framework HTTP:** possível, mas a stack do trabalho já admite Flask e o módulo tem implementação baseada nele.

## Consequências

### Positivas

- Regras de multa podem ser testadas sem fazer uma requisição HTTP.
- Os testes com o cliente de Flask verificam o contrato dos endpoints.
- A API pode mudar o formato de resposta sem mover a regra de quitação para a rota.

### Negativas

- Cada caso de uso exposto requer testes e integração entre endpoint e serviço.
- É necessário manter consistente o tratamento de erros entre domínio, serviço e API.

## Evidências

- O histórico do repositório contém implementação e testes da API Flask de multas; Ana deve confirmar o hash exato do commit antes do commit do ADR.
- A regra definida para o domínio prevê que uma multa só fica quitada quando o pagamento atende ao valor devido; o ADR final deve citar o arquivo e o teste que comprovam esse comportamento, se já estiverem implementados.
