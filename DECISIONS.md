# DECISIONS

## Ana Laura

### Fase 1 — Checkpoint 1

#### Implementação

23 - 09 - 2026 e 25 - 09 - 2026
`2d34527` — chore: inicializa pacote de dominio
`1956c77` — chore: inicializa pacote de adaptadores
`362f17e` — chore: arquivo de registros de decisoes individuais criado
`abdc50e` — chore: arquivo init.py da biblioteca criado
`d0b2356` — chore: arquivos de requirements criado
Criei a estrutura de pastas do meu agregado e o arquivo de decisões individuais. Também adicionei as dependências iniciais do projeto.

28 - 09 - 2026
`d64eec2` — feat: entidades multa e pagamento criadas
Desenvolvi a raiz de agregado `Multa` e o value object `Pagamento`. A classe principal agora protege a invariante, alterando o status apenas com o pagamento total.

#### Arquivos

- `src/biblioteca/domain/model.py`
- `tests/unit/test_multas.py`
- `requirements.txt`
- `DECISIONS.md`

#### Testes

28 - 09 - 2026 Criei testes unitários para garantir que a regra de quitação da multa funciona. Eles validam tanto pagamentos exatos quanto pagamentos insuficientes.

#### Decisão de projeto

28 - 09 - 2026 Modelei `Pagamento` como Value Object por ser apenas um registro transacional imutável. Mantive a checagem de quitação dentro de `Multa` para não vazar a regra de negócio.

### Fase 1 — Checkpoint 2

#### Implementação

28 - 09 - 2026
`2392022` — feat: interface de repositorio fake para as multas criado
`2dd4b59` — fix: correção na busca no repository.py
Criei as interfaces do repositório de multas e a versão Fake em memória. Troquei o ID na busca aqui, gerando um bug que só encontrei depois.

29 - 09 - 2026
`39f04f5` — feat: mapeamento orm de multa e pagamento criados
Fiz o mapeamento das entidades para o banco de dados usando SQLAlchemy. Configurei as tabelas de multas e pagamentos de forma imperativa.

#### Arquivos

- `src/biblioteca/adapters/__init__.py`
- `src/biblioteca/adapters/orm.py`
- `src/biblioteca/adapters/repository.py`

#### Testes

(Os testes de integração do ORM foram consolidados junto à criação do repositório fake e do mapeamento).

#### Decisão de projeto

29 - 09 - 2026 Isolei o mapeamento no adapter usando o SQLAlchemy de forma imperativa. Isso manteve meu domínio puro e sem dependências diretas da infraestrutura.

### Fase 1 — Entrega

#### Implementação

29 - 09 - 2026 `2e276da` — fix: correção da funca de busca no repositorio fake (multa)
Consertei o `FakeMultaRepository`, que buscava a multa pelo `id_leitor` em vez de `id_multa`. O erro estourou enquanto eu implementava os testes da camada de serviço.

29 - 09 - 2026
`433bcd6` — feat: service layer criada
`b9de837` — feat: api de processamento de pagamento criada
Construí o service para orquestrar a baixa da multa e criei o endpoint POST no Flask. Agora a API recebe a requisição e salva as alterações no repositório.

#### Arquivos

- `src/biblioteca/service_layer/services.py`
- `src/biblioteca/entrypoints/flask_app.py`
- `tests/unit/test_services.py`

#### Testes

29 - 09 - 2026 Fiz o teste unitário do service, que me salvou e ajudou a achar o erro do repositório fake. Depois da correção, o fluxo passou a rodar perfeitamente.

#### Decisão de projeto

29 - 09 - 2026 Deixei o service apenas orquestrando chamadas entre API e repositório. Toda a regra de validação do valor continuou presa com segurança na entidade `Multa`.