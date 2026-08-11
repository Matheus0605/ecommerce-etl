# 🛒 E-commerce ETL Pipeline

Pipeline ETL desenvolvido em **Python** para ingestão, profiling, validação, transformação e preparação de dados de um cenário de e-commerce.

O projeto simula um ambiente de dados com **10 mil clientes, 50 mil produtos e 1 milhão de pedidos**, incluindo a geração proposital de inconsistências para demonstrar práticas de **Data Quality, tratamento de dados inválidos, quarantine e testes automatizados**.

---

## 🎯 Objetivo

Construir um pipeline ETL capaz de:

* Extrair grandes volumes de dados em CSV;
* Realizar Data Profiling;
* Identificar problemas de qualidade;
* Validar integridade referencial;
* Aplicar regras de negócio;
* Separar registros inválidos;
* Transformar e enriquecer dados;
* Calcular métricas derivadas;
* Automatizar validações com Pytest;
* Preparar os dados para uma etapa posterior de carga em banco de dados.

---

## 🏗️ Arquitetura

```text
                    ┌─────────────────┐
                    │  Data Generator │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   CSV / RAW     │
                    │                 │
                    │ Customers       │
                    │ Products        │
                    │ Orders          │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Data Profiling  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Data Quality   │
                    │                 │
                    │ Nulls           │
                    │ Duplicates      │
                    │ Referential     │
                    │ Business Rules  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Transform     │
                    │                 │
                    │ Customers       │
                    │ Products        │
                    │ Orders          │
                    └────────┬────────┘
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
          ┌─────────────┐         ┌─────────────┐
          │    CLEAN    │         │  QUARANTINE │
          │    DATA     │         │    DATA     │
          └─────────────┘         └─────────────┘
```

---

## 📊 Volume de dados

| Dataset   | Registros |
| --------- | --------: |
| Customers |   10.000+ |
| Products  |    50.000 |
| Orders    | 1.000.000 |

Os dados são gerados automaticamente para permitir testes com volume significativo sem depender de dados reais.

---

## 🔎 Data Profiling

O pipeline realiza uma análise inicial dos datasets verificando:

* Quantidade de registros;
* Quantidade de colunas;
* Tipos de dados;
* Valores nulos;
* Registros duplicados;
* Integridade dos identificadores.

Exemplo:

```text
DATASET: ORDERS

Linhas: 1,000,000
Colunas: 6

Valores nulos:
id             0
cliente_id     0
produto_id     0
quantidade     0
data_pedido    0
status         0

Registros duplicados: 0
```

---

## 🛡️ Data Quality

O projeto possui uma etapa específica para identificar inconsistências nos dados.

### Integridade referencial

São verificadas relações como:

```text
orders.cliente_id → customers.id
orders.produto_id → products.id
```

### Regras de negócio

Também são verificadas regras como:

```text
preço > 0
estoque >= 0
quantidade > 0
```

Durante os testes de qualidade foram introduzidas inconsistências propositalmente.

Resultado identificado:

```text
Pedidos com cliente inexistente: 100
Pedidos com produto inexistente: 0

Produtos com preço inválido: 50
Produtos com estoque inválido: 50

Pedidos com quantidade inválida: 100
```

---

## 🧪 Testes automatizados

O projeto utiliza **Pytest** para validar as principais etapas do pipeline.

Atualmente:

```text
10 passed
```

Os testes cobrem:

* Extração de CSV;
* Transformação de Customers;
* Transformação de Products;
* Transformação de Orders;
* Regras de negócio;
* Quarantine;
* Integridade dos relacionamentos;
* Cálculo do valor total dos pedidos.

Execução:

```bash
python -m pytest
```

Resultado:

```text
10 passed
```

---

## 🔄 Transformações

### Customers

São aplicadas validações relacionadas aos clientes e seus dados cadastrais.

### Products

São validados:

```text
preço
estoque
```

Produtos inválidos são direcionados para quarantine.

### Orders

Os pedidos são enriquecidos através do relacionamento com Products.

O pipeline calcula:

```text
valor_total = quantidade × preco_unitario
```

Exemplo:

```text
Produto: Notebook
Quantidade: 2
Preço unitário: R$ 3.500,00

Valor total:
R$ 7.000,00
```

---

## 🚨 Quarantine

Registros que não atendem às regras críticas de qualidade são separados do fluxo principal.

Exemplo de motivos:

```text
customer_not_found
product_not_found
invalid_quantity
invalid_price
invalid_stock
```

Isso permite preservar os dados inválidos para posterior investigação, em vez de simplesmente descartá-los.

---

## 📈 Execução atual

Com os dados inconsistentes inseridos propositalmente, o pipeline apresentou:

```text
Customers: 10,020
Products: 50,000
Orders: 1,000,000

Customers válidos: 9,950
Customers quarantine: 70

Products válidos: 49,900
Products quarantine: 100

Orders válidos: 992,899
Orders quarantine: 7,101
```

Principais motivos encontrados:

```text
customer_not_found    5,042
product_not_found     1,961
invalid_quantity         98
```

Esse resultado também revelou um importante efeito de propagação de problemas de qualidade entre datasets relacionados, que será tratado nas próximas etapas da arquitetura.

---

## 📁 Estrutura do projeto

```text
ecommerce-etl/
│
├── data/
│
├── src/
│   │
│   ├── extract/
│   │   └── csv_extractor.py
│   │
│   ├── generators/
│   │   ├── generate_data.py
│   │   └── inject_errors.py
│   │
│   ├── profiling/
│   │   ├── profile_data.py
│   │   └── data_quality.py
│   │
│   ├── transform/
│   │   ├── customers.py
│   │   ├── products.py
│   │   └── orders.py
│   │
│   └── pipeline/
│       └── transform_pipeline.py
│
├── tests/
│   ├── test_extract.py
│   ├── test_transform_customers.py
│   ├── test_transform_products.py
│   └── test_transform_orders.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Tecnologias

* **Python 3.11**
* **Pandas**
* **Pytest**
* **Faker**
* **CSV**
* **Git / GitHub**

---

## 🚀 Como executar

### 1. Clonar o projeto

```bash
git clone https://github.com/Matheus0605/ecommerce-etl.git
```

```bash
cd ecommerce-etl
```

### 2. Criar ambiente virtual

Windows:

```bash
python -m venv .venv
```

Ativar:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Gerar os dados

```bash
python src/generators/generate_data.py
```

### 5. Inserir inconsistências

```bash
python src/generators/inject_errors.py
```

### 6. Executar Data Profiling

```bash
python src/profiling/profile_data.py
```

### 7. Executar Data Quality

```bash
python src/profiling/data_quality.py
```

### 8. Executar os testes

```bash
python -m pytest
```

### 9. Executar o pipeline

```bash
python -m src.pipeline.transform_pipeline
```

---

## 🧠 Conceitos demonstrados

Este projeto foi desenvolvido com foco em conceitos utilizados em ambientes reais de engenharia e análise de dados:

* ETL;
* Data Profiling;
* Data Quality;
* Integridade referencial;
* Regras de negócio;
* Data Transformation;
* Data Enrichment;
* Quarantine;
* Testes automatizados;
* Processamento de grandes volumes;
* Separação de responsabilidades;
* Rastreabilidade de problemas;
* Validação de pipelines.

---

## 🔮 Próximas etapas

O projeto continuará evoluindo para uma arquitetura ETL mais próxima de um ambiente produtivo.

### Roadmap

* [x] Geração dos datasets
* [x] Injeção de inconsistências
* [x] Data Profiling
* [x] Data Quality
* [x] Extract
* [x] Transform Customers
* [x] Transform Products
* [x] Transform Orders
* [x] Testes automatizados
* [ ] Classificação `VALID / WARNING / QUARANTINE`
* [ ] Métricas de performance
* [ ] Logging estruturado
* [ ] Load em PostgreSQL
* [ ] Modelagem dimensional
* [ ] Camada Silver / Gold
* [ ] Docker
* [ ] Orquestração do pipeline
* [ ] Monitoramento
* [ ] CI/CD
* [ ] Dashboard de qualidade dos dados

---

## 👨‍💻 Autor

**Matheus Pinheiro**

Projeto desenvolvido como estudo prático de **Python, ETL, Data Quality, testes automatizados e engenharia de dados**.

GitHub:

https://github.com/Matheus0605

```
```
