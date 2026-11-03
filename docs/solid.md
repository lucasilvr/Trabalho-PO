# Refatorações SOLID — Fase 2

## João Vicente Piller Menezes — Reserva

### Princípio violado

**Open/Closed Principle (OCP):** a entidade `Reserva` deveria estar aberta para extensão
(novos prazos de retirada) e fechada para modificação. Porém, o prazo de 48 horas estava
fixo dentro do método `esta_expirada`, de modo que qualquer mudança de prazo exigia
alterar a própria classe de domínio.

### Código antes

Introduzido no commit `f185330` (22/09/2026), anterior a 06/10/2026:

```python
# src/biblioteca/reservas/domain/model.py
def esta_expirada(self, data_hora_atual: datetime) -> bool:
    if self.status == "Disponivel" and self.data_disponibilizacao is not None:
        return (data_hora_atual - self.data_disponibilizacao) > timedelta(hours=48)
    return False
```

### Problema concreto

Mudança de requisito plausível: a biblioteca passa a dar prazos de retirada diferentes
conforme a categoria do leitor (por exemplo, 72 horas para professores e 48 horas para
alunos), regra que já aparece no agregado de Cadastro de Leitores (`CategoriaLeitor`).

Com o prazo fixo no código, atender esse requisito obrigaria a modificar `Reserva`
toda vez que um novo prazo surgisse, misturando na entidade uma regra que pertence
à configuração de cada reserva. Além disso, o valor `48` não era persistido, então
não havia como uma reserva carregada do banco "lembrar" o prazo com que foi criada.

### Refatoração

Commit "depois": `14d6d57`

- `domain/model.py`: o prazo virou o atributo `prazo_retirada_horas`, recebido no
  construtor, com o valor padrão `PRAZO_RETIRADA_PADRAO_HORAS = 48`. O método
  `esta_expirada` passou a usar esse atributo.
- `adapters/orm.py`: nova coluna `prazo_retirada_horas` na tabela `reservas`, com
  valor padrão 48 no banco, para que reservas já existentes continuem válidas.
- `service_layer/services.py`: `reservar_livro` aceita um `prazo_retirada_horas`
  opcional.
- `entrypoints/flask_app.py`: o endpoint `POST /reservas` aceita o campo opcional
  `prazo_retirada_horas`.

```python
# src/biblioteca/reservas/domain/model.py (depois)
def esta_expirada(self, data_hora_atual: datetime) -> bool:
    if self.status == "Disponivel" and self.data_disponibilizacao is not None:
        return (data_hora_atual - self.data_disponibilizacao) > timedelta(hours=self.prazo_retirada_horas)
    return False
```

Agora um novo prazo é atendido apenas criando a reserva com outro valor, sem
modificar a classe `Reserva`.

### Como os testes garantiram o comportamento

- Os 16 testes existentes do módulo (unitários, de integração e e2e) continuaram
  passando **sem nenhuma alteração**, inclusive `test_reserva_expira_apos_48_horas_disponivel`
  e o e2e `test_happy_path_transfere_reserva_apos_48_horas`. Isso comprova que o
  comportamento padrão de 48 horas foi preservado.
- Foram adicionados 5 testes para o novo requisito: prazo padrão de 48 horas,
  reserva de 72 horas que não expira com 49 horas e expira com 73 horas, serviço
  com prazo personalizado, persistência do prazo no banco e leitura de uma reserva
  inserida sem prazo (que recebe o padrão de 48 horas).

### Custo da refatoração

- Um atributo a mais na entidade, uma coluna a mais na tabela e um parâmetro opcional
  a mais no serviço e na API.
- O valor padrão precisa existir em dois lugares (na constante do domínio e no
  `server_default` do banco). Para evitar divergência, o ORM usa a própria constante
  `PRAZO_RETIRADA_PADRAO_HORAS`.

O custo é pequeno e compensa: o requisito de prazos por categoria passa a ser atendido
sem modificar a entidade, e o comportamento antigo fica intacto por padrão. Quem decide
o prazo de cada leitor ainda não está definido. Essa escolha pode virar um padrão GoF
(por exemplo, Strategy) no checkpoint 3.
