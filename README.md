## 📌 Descrição
Projeto em desenvolvimento com foco na construção de um pipeline de dados para ingestão, tratamento e disponibilização de dados da API Random Users Generator.

## 🏗️ Status
🚧 Em desenvolvimento — estrutura inicial.

## 📂 Estrutura
data-pipeline-usuarios/ 
│ 
├── data/ 
│ ├── raw/ # Dados brutos (ingestão) 
│ ├── processed/ # Dados tratados  
├── notebooks/ 
├── src/
├── tests/
├── README.md 
├── requirements.txt


## 🔄 Pipeline de Dados

O pipeline segue as etapas:

1. **Extract**
   - Consumo da API Random User
   - Armazenamento dos dados brutos em JSON

2. **Transform**
   - Tratamento e normalização dos dados
   - Conversão para formato tabular

3. **Load**
   - Persistência dos dados tratados em CSV


## ⚙️ Configuração
Variáveis de ambiente necessárias:
- API_KEY