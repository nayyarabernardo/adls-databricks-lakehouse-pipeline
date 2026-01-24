# BikeStore Lakehouse – Data Foundation

Este projeto implementa um **Data Lakehouse** para o domínio **BikeStore**, com foco em **qualidade, rastreabilidade, governança e escalabilidade**, servindo como **fundação para análises, métricas de negócio e produtos analíticos**.

A arquitetura segue o padrão **Medallion (Bronze → Silver → Gold)**, com ingestão estruturada, validações explícitas e transformações orientadas a domínio.

---

## Objetivo do Projeto

* Centralizar dados operacionais do BikeStore em um **Lakehouse**
* Garantir **dados confiáveis (Trusted Data)** na camada Silver
* Disponibilizar dados prontos para consumo na camada Gold, suportando:

  * métricas de negócio
  * análises analíticas
  * produtos de dados
  * evolução para Feature Store e ML

Este projeto foi desenhado como um **produto de dados de escopo fechado**, com entidades bem definidas, pipelines explícitos e foco em previsibilidade operacional.

---

## Arquitetura Geral

### Visão Conceitual (Lakehouse / Medallion)

![](https://github.com/nayyarabernardo/adls-databricks-lakehouse-pipeline/blob/main/img/azure.png)

---

### Visão Técnica do Pipeline

Abaixo está a arquitetura real de execução dos pipelines, refletindo tabelas, validações e dependências entre camadas:

![](https://github.com/nayyarabernardo/adls-databricks-lakehouse-pipeline/blob/main/img/arq.png)

---

### Tecnologias Utilizadas

* **Databricks**
* **Apache Spark**
* **Delta Lake**
* **Azure Data Lake Storage Gen2**
* **Databricks Jobs (YAML)**

---

## Estrutura do Repositório

```
data-lake-databricks/
├── README.md
├── src/
│   ├── config/
│   │   └── 01.settings.py              # Env vars, paths por camada
│   ├── common/
│   │   └── utils.py                    # Logging, helpers Spark
│   ├── bronze/
│   │   ├── ingest.py                  # Raw load + metadata
│   │   └── upload.py                  # Escrita Delta Bronze
│   ├── silver/
│   │   ├── base.py                    # Regras genéricas
│   │   ├── registry.py
│   │   ├── categories.py
│   │   ├── customers.py
│   │   ├── order_items.py
│   │   ├── orders.py
│   │   ├── products.py
│   │   ├── brands.py 
│   │   ├── staffs.py
│   │   ├── stores.py
│   │   └── stocks.py
│   ├── gold/
│   │   ├── treat.py                   # Regras de negócio / agregações
│   │   └── upload.py                  # Escrita Delta Gold
├── notebooks/
│   ├── 00_setup/
│   │   └── 00_infrastructure.ipynb
│   ├── 01_bronze/
│   │   ├── 01_bronze_pipeline.ipynb  
│   │   └── 02_validation_bronze.ipynb
│   ├── 02_silver/
│   │   └── 01_silver_pipeline.ipynb  
│   └── 03_gold/
│       └── 01_gold_pipeline.ipynb
├── resources/
│   └── jobs/
│       └── bikestore_lakehouse.yml
├── tests/
└── data/
```

---

## Bronze Layer – Ingestão

### Descrição

A camada Bronze é responsável por:

* ingestão de dados brutos (JSON)
* preservação do formato original
* rastreabilidade completa
* armazenamento em **Delta Lake**
* ingestão incremental

Cada tabela é ingerida de forma **independente**, via parâmetro `table_name`.

### Tabelas Bronze

* brands
* categories
* customers
* order_items
* orders
* products
* staffs
* stocks
* stores

### Execução

Notebook:

```
notebooks/01_bronze/01_bronze_pipeline
```

Parâmetro:

```json
{
  "table_name": "customers"
}
```

---

## Validação Bronze

Após a ingestão, um job de validação executa verificações básicas:

* existência de dados
* leitura correta das tabelas Delta
* consistência mínima de schema

Notebook:

```
notebooks/01_bronze/02_validation_bronze
```

---

## Silver Layer – Dados Confiáveis (Trusted Data)

### Princípios da Silver

A camada Silver aplica regras de **qualidade e padronização**, garantindo:

* limpeza de dados
* remoção de registros inválidos
* padronização de schemas
* deduplicação
* inclusão de metadados de ingestão

Cada tabela Bronze gera **uma tabela Silver correspondente**.

---

### Padrão de Implementação

* Regras genéricas: `silver/base.py`
* Regras específicas por entidade: arquivos dedicados

Exemplo:

```
src/silver/customers.py
```

Funções comuns:

* `read_bronze`
* `add_ingestion_columns`
* `write_silver`

---

### Metadados

Todas as tabelas Silver possuem:

| Coluna       | Descrição                       |
| ------------ | ------------------------------- |
| ingestion_ts | Timestamp da ingestão na Silver |

Essas colunas suportam:

* auditoria
* troubleshooting
* rastreabilidade ponta a ponta

---

## Gold Layer – Camada de Negócio

A camada Gold consolida os dados Silver em **tabelas orientadas ao consumo**, aplicando regras de negócio, métricas e agregações.

Características:

* métricas prontas para BI
* dados agregados e otimizados
* menor cardinalidade
* foco em consumo analítico

Implementação:

* regras em `src/gold/treat.py`
* escrita Delta em `src/gold/upload.py`
* notebooks em `notebooks/03_gold`

---

## Orquestração (Databricks Jobs)

O pipeline é orquestrado via **Databricks Jobs (YAML)**, com:

* uma task por tabela
* dependências explícitas entre camadas
* execução paralela quando possível

Fluxo:

1. Ingestão Bronze
2. Validação Bronze
3. Transformação Silver
4. Transformação Gold

---

## Estratégia de Escopo

Este projeto segue o conceito de:

> **Produto de Dados de Escopo Fechado**

Benefícios:

* entidades bem definidas
* pipelines previsíveis
* menor custo operacional
* fácil manutenção

O desenho permite evolução para:

* novas entidades
* métricas adicionais
* Feature Store
* modelos de Machine Learning

