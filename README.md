# Data Pipeline de Usuários

Pipeline de dados desenvolvido em Python para extrair informações da Random User API, armazenar os dados brutos, aplicar validações, carregar os registros no SQL Server e disponibilizar uma camada analítica.

O projeto começou como uma integração simples com API e vem sendo evoluído de forma incremental, com foco em práticas utilizadas em Engenharia de Dados, como rastreabilidade, controle de execução, qualidade de dados, idempotência, logs e separação em camadas.

## Arquitetura atual

```text
Random User API
        ↓
Extração
        ↓
Raw — JSON original
        ↓
Transformação e validação
        ↓
Bronze — CSV com status OK/NOK
        ↓
Staging — todos os registros do lote
        ↓
Silver — somente registros válidos e únicos
        ↓
Gold — view com regras de negócio
```

## Como o pipeline funciona

### 1. Extração

O módulo de extração consulta a Random User API e solicita dados de usuários brasileiros.

Nesta etapa são registrados:

- início da chamada;
- quantidade de registros recebidos;
- retorno vazio;
- erros de comunicação com a API.

### 2. Persistência dos dados brutos

A resposta da API é armazenada em JSON sem alterações.

Essa camada preserva o dado original recebido da fonte e permite reprocessar uma execução sem realizar uma nova chamada à API.

### 3. Transformação e validação

Os dados do JSON são normalizados com Pandas e convertidos para uma estrutura tabular.

Durante a transformação, são aplicadas validações básicas:

- ID do usuário obrigatório;
- formato mínimo de e-mail;
- data de nascimento não pode estar no futuro.

Cada registro recebe um status:

- `OK`: registro aprovado para a camada Silver;
- `NOK`: registro mantido para análise, mas impedido de avançar.

Todos os registros são gravados em um único CSV, incluindo os dados válidos e inválidos.

### 4. Carga no SQL Server

O CSV é carregado inicialmente na tabela `STAGING_USERS`.

A staging mantém todos os registros do lote, inclusive os classificados como `NOK`.

Depois da carga, um `MERGE` envia para a `SILVER_USERS` apenas os registros que:

- pertencem à execução atual;
- possuem status `OK`;
- ainda não existem na Silver.

A tabela Silver utiliza o ID do usuário como chave primária, evitando duplicidades em reprocessamentos.

### 5. Camada Gold

A camada Gold é disponibilizada por meio de uma view no SQL Server.

Ela aplica regras de negócio e tratamentos como:

- nome completo;
- tradução do gênero;
- endereço completo;
- cálculo atualizado da idade;
- tempo de cadastro;
- idade no momento do cadastro;
- status da conta;
- faixa etária.

## Controle de execução

Cada execução recebe um `run_id` gerado com UUID.

O identificador acompanha os registros no CSV, na staging e na Silver, permitindo identificar em qual execução cada dado foi processado.

Exemplo:

```text
run_239389779ece44279c2affc007f5c7ac
```

O pipeline também registra métricas da execução, como:

- quantidade recebida da API;
- registros válidos;
- registros inválidos;
- IDs distintos;
- registros inseridos na staging;
- registros inseridos na Silver;
- registros rejeitados;
- tempo total de execução;
- status final.

## Idempotência

A carga da camada Silver é idempotente.

Isso significa que o mesmo conjunto de dados pode ser processado novamente sem gerar usuários duplicados.

A proteção acontece por meio de:

- filtro pelo `run_id` atual;
- deduplicação da origem com `ROW_NUMBER`;
- comparação pelo ID do usuário;
- `MERGE` com inserção somente de registros inexistentes;
- chave primária na tabela Silver.

A staging pode armazenar diferentes execuções do mesmo conjunto de dados, enquanto a Silver mantém apenas uma ocorrência de cada usuário.

## Estrutura do projeto

```text
data-pipeline-usuarios/
│
├── data/
│   ├── raw/                   # Respostas originais da API em JSON
│   ├── bronze/                # Arquivos CSV transformados
│   └── pipeline_state/        # Controle de arquivos processados
│
├── log/                       # Logs das execuções
│
├── sql/
│   ├── ddl/
│   │   └── create_tables.sql  # Criação das tabelas e estruturas
│   │
│   ├── dml/
│   │   └── insert_users.sql
│   │
│   └── queries/
│       └── qrys_tests.sql
│
├── src/
│   ├── extract.py             # Extração da API
│   ├── load.py                # Persistência do JSON e controle de arquivos
│   ├── transform.py           # Normalização e validação
│   ├── load_sql.py            # Carga na staging e Silver
│   ├── logging_config.py      # Configuração centralizada de logs
│   ├── helpers.py             # Funções auxiliares
│   └── main.py                # Orquestração do pipeline
│
├── notebooks/
├── requirements.txt
├── .gitignore
└── README.md
```

## Tecnologias utilizadas

- Python
- Pandas
- Requests
- PyODBC
- SQL Server
- Python Dotenv
- Biblioteca Logging
- UUID
- Git e GitHub

## Funcionalidades implementadas

- Consumo de API REST;
- persistência dos dados brutos em JSON;
- transformação e normalização com Pandas;
- geração de CSV;
- validação de ID, e-mail e data de nascimento;
- classificação dos registros em `OK` e `NOK`;
- carga em lote no SQL Server;
- arquitetura com staging, Silver e Gold;
- carga idempotente com `MERGE`;
- deduplicação por ID;
- identificação da execução com `run_id`;
- tratamento de valores nulos entre Pandas e SQL Server;
- logs no terminal e em arquivo;
- rotação dos arquivos de log;
- métricas de execução;
- controle de arquivos processados;
- uso de variáveis de ambiente;
- organização modular do código.

## Configuração do ambiente

Crie um arquivo `.env` na raiz do projeto com as informações de conexão ao SQL Server:

```env
DB_DRIVER={ODBC Driver 18 for SQL Server}
DB_SERVER=nome_do_servidor
DB_NAME=ANALYTICS_HUB
DB_TRUSTED=yes
```

O arquivo `.env` não deve ser enviado ao GitHub.

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie as tabelas utilizando:

```text
sql/ddl/create_tables.sql
```

Depois, execute o pipeline:

```bash
python src/main.py
```

## Exemplo de log

```text
2026-08-02 09:23:41 | INFO | main | Pipeline iniciado
2026-08-02 09:23:42 | INFO | conexao_api_clientes | Recebidos API: 100
2026-08-02 09:23:42 | INFO | transformacao_clientes | Válidos: 100
2026-08-02 09:23:42 | WARNING | transformacao_clientes | Inválidos: 0
2026-08-02 09:23:42 | INFO | insert_db | Insert STAGING_USERS - Registros: 100
2026-08-02 09:23:42 | INFO | insert_db | Insert SILVER_USERS - Registros: 100
2026-08-02 09:23:42 | INFO | main | Status: Sucesso
2026-08-02 09:23:42 | INFO | main | Execução: 1.01 segundos
```

## Próximas evoluções

As próximas melhorias serão adicionadas de forma incremental, sem alterar várias partes do pipeline ao mesmo tempo.

Entre os próximos passos estão:

- melhorar o tratamento de falhas entre as etapas;
- interromper corretamente o pipeline quando uma etapa falhar;
- registrar status de erro e duração até a falha;
- ampliar as regras de qualidade de dados;
- melhorar o controle de registros rejeitados;
- criar testes automatizados;
- avaliar orquestração com Airflow;
- explorar processamento com Databricks e PySpark;
- avaliar o uso de dbt na camada de transformação analítica.

## Objetivo do projeto

O objetivo deste repositório é registrar a evolução prática de um pipeline de dados.

Mais do que consumir uma API, o projeto busca trabalhar problemas comuns de Engenharia de Dados, como:

- reprocessamento;
- dados inválidos;
- duplicidade;
- rastreabilidade;
- falhas de execução;
- qualidade de dados;
- separação de responsabilidades;
- organização em camadas.

As melhorias são implementadas e documentadas gradualmente, preservando o histórico de evolução do projeto.
