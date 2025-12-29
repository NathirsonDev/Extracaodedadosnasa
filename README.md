# ☄️ NASA Asteroid Data Pipeline (ETL & Analytics)

Este projeto é um pipeline de Engenharia de Dados ponta-a-ponta que extrai, transforma e carrega (ETL) dados de objetos próximos à Terra (NEOs) utilizando a API oficial da NASA.

O sistema foi desenhado para ser resiliente, automatizado e **idempotente**, garantindo a integridade dos dados históricos num banco de dados SQL local para análise de risco e visualização.

## 🏗️ Arquitetura do Projeto

`NASA API (JSON)` -> `Python (Extract & Transform)` -> `SQLite (Load)` -> `SQLAlchemy (Query)` -> `Matplotlib (Viz)`

O fluxo de dados segue os seguintes passos:
1.  **Ingestão:** Conexão com a API `NeoWs` da NASA com gestão de rate limits e paginação temporal.
2.  **Processamento:** Limpeza de JSON aninhado e tipagem de dados com Pandas.
3.  **Idempotência:** Verificação prévia no banco de dados para evitar duplicidade de registros (Upsert lógico).
4.  **Armazenamento:** Persistência em banco de dados relacional (SQLite).
5.  **Analytics:** Consultas SQL para métricas de negócio (tamanho médio, periculosidade, tendências).

## 🛠️ Tech Stack

* **Linguagem:** Python 3.x
* **Manipulação de Dados:** Pandas
* **Banco de Dados:** SQLite & SQLAlchemy
* **Requisições HTTP:** Requests
* **Visualização:** Matplotlib
* **Gestão de Ambiente:** Python-dotenv

## 🚀 Como Rodar o Projeto

### Pré-requisitos
* Python 3 instalado.
* Uma chave de API da NASA (Grátis em: https://api.nasa.gov/).

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone [https://github.com/SEU_USUARIO/nome-do-repo.git](https://github.com/SEU_USUARIO/nome-do-repo.git)
   cd nome-do-repo
