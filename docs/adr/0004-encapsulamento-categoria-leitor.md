# ADR 0001: Encapsulamento da Categoria do Leitor como Value Object

**Data:** 29-10-2026
**Autor:** Isabella Vieira da Motta

## Contexto
O sistema precisa garantir que um leitor não ultrapasse o limite de empréstimos permitido, que varia de acordo com a sua categoria (ex: Aluno, Professor). Deixar essa regra solta na camada de serviço poderia gerar inconsistências, e criar uma tabela isolada no banco de dados para "Categorias" exigiria JOINs desnecessários para uma validação tão simples.

## Decisão
Decidimos modelar `CategoriaLeitor` como um *Value Object* dentro da camada de domínio, e mapeá-lo no SQLAlchemy utilizando o padrão *Composite* diretamente na tabela `leitores`.

## Consequências
* **Positivas:** A regra de negócio (invariante de limites) fica fortemente encapsulada no agregado. O banco de dados fica otimizado (uma única tabela `leitores`), sem comprometer a pureza do modelo de domínio.
* **Negativas:** Exigiu um conhecimento mais profundo da API imperativa do SQLAlchemy (`mapper_registry.composite`), o que aumentou levemente a curva de aprendizado inicial.