# 📊 Data Pipeline - Usuários (Random User API)

## 📌 Visão Geral

Projeto de engenharia de dados desenvolvido em Python com foco na construção de um pipeline completo para ingestão, tratamento, persistência e disponibilização de dados.

O pipeline consome dados da API Random User Generator, armazena os dados brutos em JSON, realiza transformações e normalizações em CSV e posteriormente carrega os dados em SQL Server.

O objetivo do projeto é evoluir gradualmente para uma arquitetura mais robusta de engenharia de dados, incluindo controle de execução, deduplicação, idempotência e modelagem em múltiplas camadas.

---

## 🏗️ Arquitetura do Pipeline

Fluxo atual do pipeline:

```text
Random User API
        ↓
Extract
        ↓
JSON Raw Layer
        ↓
Transform
        ↓
CSV Processed Layer
        ↓
SQL Server Staging


🔄 Etapas do Pipeline

🔹 Extract
Consumo da API Random User Generator API
Coleta de dados de usuários brasileiros
Validação de retorno da API
Logging da execução

🔹 Load Raw
Persistência dos dados brutos em JSON
Garantia de rastreabilidade da ingestão

🔹 Transform
Normalização dos dados
Estruturação tabular com pandas
Geração de arquivos CSV
Inclusão de metadados de execução

🔹 Load SQL
Leitura do CSV processado
Inserção em batch no SQL Server
Utilização de variáveis de ambiente via .env


📂 Estrutura do Projeto
data-pipeline-usuarios/
│
├── data/
│   ├── raw/                  # Dados brutos em JSON
│   ├── bronze/               # Dados transformados em CSV
│   └── pipeline_state/       # Controle de arquivos processados
│
├── log/                      # Logs das execuções
│
├── sql/
│   ├── ddl/
│   │   └── create_tables.sql
│   │
│   ├── dml/
│   │   └── insert_users.sql
│   │
│   └── queries/
│       └── qrys_tests.sql
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── load_sql.py
│   ├── logger.py
│   ├── helpers.py
│   └── main.py
│
├── notebooks/
├── requirements.txt
└── README.md



⚙️ Tecnologias Utilizadas
Python
pandas
requests
pyodbc
SQL Server
dotenv


📋 Funcionalidades Implementadas
✔️ Consumo de API REST
✔️ Persistência em JSON
✔️ Transformação tabular com pandas
✔️ Geração de CSV
✔️ Inserção em batch no SQL Server
✔️ Logging customizado
✔️ Uso de variáveis de ambiente
✔️ Controle de arquivos processados
✔️ Estrutura modularizada


🚧 Próximas Evoluções
Implementação de MERGE no SQL Server
Controle de duplicidade
Idempotência do pipeline
Modelagem tipada de tabelas analíticas
Controle de execução do pipeline
Melhorias de observabilidade


🎯 Objetivo do Projeto

Este projeto tem como objetivo simular cenários reais de engenharia de dados, evoluindo gradualmente desde pipelines simples até arquiteturas mais robustas e próximas de ambientes produtivos.

