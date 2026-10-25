# Data Pipeline de Usuários

Projeto de Engenharia de Dados e Analytics Engineering desenvolvido para praticar a construção e evolução de pipelines, desde a ingestão de dados até a preparação de modelos analíticos.

A aplicação consome dados fictícios da Random User API, realiza transformações e validações com Python, utiliza Apache Airflow para orquestração e SQL Server para persistência. O projeto também está sendo expandido para BigQuery e dbt, com foco em transformação SQL, qualidade de dados e modelagem analítica.

O desenvolvimento é incremental, permitindo aplicar novos conceitos sem descartar as implementações anteriores.

## Arquitetura

**Pipeline operacional — Python, Airflow e SQL Server**

```text
Random User API
       |
       v
Apache Airflow
       |
       v
Raw (JSON original)
       |
       v
Transformação com Pandas
       |
       v
Bronze (CSV - OK/NOK)
       |
       v
SQL Server
       |
       +-- STAGING_USERS
       |
       +-- SILVER_USERS
       |
       +-- PIPELINE_RUNS
```

**Ambiente analítico — BigQuery e dbt**

```text
CSV Bronze
    |
    v
Carga manual no BigQuery
    |
    v
bronze_usuarios
    |
    v
dbt - Staging
    |
    v
stg_usuarios (View)
```

Atualmente, os dois fluxos estão separados. O Airflow executa o pipeline com SQL Server, enquanto o BigQuery recebe uma amostra do CSV para o desenvolvimento dos modelos dbt.

A integração automática com BigQuery está planejada para uma etapa posterior.

## Funcionalidades implementadas

### Ingestão e transformação

A extração consulta a Random User API e armazena a resposta original em JSON na camada Raw.

Os dados são normalizados com Pandas, convertidos para CSV e submetidos a validações de ID, formato de e-mail e data de nascimento. Cada registro recebe uma classificação `OK` ou `NOK`, preservando também os registros inválidos para análise.

### Persistência no SQL Server

Os dados são carregados inicialmente na `STAGING_USERS`, que mantém os registros dos lotes processados.

Um `MERGE` insere na `SILVER_USERS` somente registros classificados como `OK` e ainda inexistentes pelo identificador do usuário. A combinação de deduplicação com `ROW_NUMBER`, comparação por ID e chave primária evita usuários duplicados na Silver.

A Staging mantém o histórico das cargas e pode conter registros de diferentes execuções.

### Orquestração e monitoramento

O Apache Airflow coordena as etapas de extração, transformação, carga e finalização.

Cada execução recebe um `run_id`, utilizado para rastrear o processamento entre as etapas.

A tabela `PIPELINE_RUNS` registra o início, término, duração e status da execução (`RUNNING`, `SUCCESS` ou `ERROR`).

O pipeline também possui tratamento de exceções, logs e recuperação automática de falhas transitórias na extração, com até duas novas tentativas.

### Transformações com dbt

O BigQuery contém a tabela `bronze_usuarios`, carregada inicialmente com uma amostra de 1.000 registros.

O dbt utiliza essa tabela como Source e materializa o primeiro modelo, `stg_usuarios`, como uma view.

O modelo realiza renomeação de colunas e conversão de tipos, preparando os dados para futuras transformações analíticas.

A execução foi validada com 1.000 registros, 1.000 IDs distintos e campo de nascimento convertido para `DATE`.

## Tecnologias

| Tecnologia | Utilização |
|---|---|
| Python e Pandas | Extração, normalização e validação |
| Apache Airflow | Orquestração e recuperação de falhas |
| SQL Server | Staging, Silver e controle de execuções |
| BigQuery | Armazenamento para análise na nuvem |
| dbt Core | Transformações SQL e organização dos modelos |
| Docker | Ambiente local do Airflow |
| Git e GitHub | Versionamento e histórico de evolução |

## Estrutura principal

```text
data-pipeline-usuarios/
|
|-- dags/
|   `-- pipeline_usuarios_extract.py
|
|-- src/
|   |-- extract.py
|   |-- transform.py
|   |-- load.py
|   |-- load_sql.py
|   |-- run_control.py
|   `-- main.py
|
|-- data/
|   |-- raw/
|   `-- bronze/
|
|-- sql/
|   |-- ddl/
|   |-- dml/
|   `-- qrys/
|       `-- ae01_profile_staging.sql
|
|-- dbt_usuarios/
|   |-- dbt_project.yml
|   `-- models/
|       `-- staging/
|           |-- sources.yml
|           `-- stg_usuarios.sql
|
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## Execução

### Pipeline Python

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure o `.env` com os parâmetros de conexão ao SQL Server e prepare as tabelas conforme `sql/ddl/create_tables.sql`.

Para execução local:

```bash
python src/main.py
```

O pipeline também pode ser executado pela DAG `pipeline_usuarios_extract` no ambiente Airflow configurado com Docker.

### dbt e BigQuery

Com o dbt instalado, as credenciais locais configuradas e a tabela de origem disponível no BigQuery, acesse:

```bash
cd dbt_usuarios
```

Valide a conexão:

```bash
dbt debug
```

Execute o modelo:

```bash
dbt run --select stg_usuarios
```

O arquivo `profiles.yml` e as credenciais Google devem permanecer fora do repositório.

## Próximas evoluções

O foco atual do projeto é Analytics Engineering. As próximas entregas serão direcionadas a:

- Testes automatizados de qualidade com dbt;
- documentação e dependências entre modelos com `ref()`;
- modelagem analítica e construção de marts;
- integração automática do pipeline com BigQuery;
- melhorias de observabilidade e idempotência.

O desenvolvimento segue uma demanda por vez, com validação técnica e versionamento de cada entrega.

## Objetivo

Este repositório documenta minha evolução prática em Engenharia de Dados e Analytics Engineering.

A proposta é consolidar conhecimentos de SQL, Python, orquestração, qualidade de dados e modelagem analítica, trabalhando problemas semelhantes aos encontrados em ambientes reais de dados.

O histórico de commits registra essa evolução, desde a integração inicial com API até a construção de uma arquitetura analítica utilizando BigQuery e dbt.