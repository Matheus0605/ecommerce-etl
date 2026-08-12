# 🛒 E-commerce ETL Pipeline

Este repositório contém um pipeline ETL em Python que simula um ambiente de e-commerce com geração volumétrica de dados, profiling, validações de qualidade, transformação, escrita em camada Silver (Parquet) e carga em um modelo dimensional (Postgres - Gold).

O objetivo principal é demonstrar boas práticas de engenharia de dados: separação de responsabilidades, testes automatizados, quarantine (registros inválidos), geração de métricas e observability mínima com um dashboard.

Principais componentes implementados:

- Gerador de dados (Faker) com injeção de inconsistências;
- Extractors/Transformers em pandas;
- Data Quality (regras, integridade referencial, quarantine);
- Escrita Silver em Parquet;
- Modelo dimensional (dim/fact) e carregamento em Postgres (Gold);
- Orquestração básica com Prefect (fluxo local); fallback para execução sequencial quando Prefect não estiver disponível;
- Logging estruturado (JSON) e métricas de qualidade (arquivo JSON);
- Dashboard rápido em Streamlit para inspeção de métricas;
- Docker + docker-compose para ambiente local (Postgres + app);
- CI básico (GitHub Actions) rodando testes e build de imagem.

---

Índice
- [Pré-requisitos](#pré-requisitos)
- [Quickstart (local)](#quickstart-local)
- [Rodando com Docker Compose](#rodando-com-docker-compose)
- [Executando o pipeline](#executando-o-pipeline)
- [Camadas Silver / Gold](#camadas-silver--gold)
- [Dashboard](#dashboard)
- [CI / Tests](#ci--tests)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Roadmap e próximos passos](#roadmap-e-próximos-passos)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

---

## Pré-requisitos

- Python 3.11
- Git
- (Opcional) Docker Desktop para ambiente local com Postgres e um container do app

Recomenda-se trabalhar com virtualenv (.venv) para isolar dependências.

---

## Quickstart (local)

1. Clone o repositório:

```bash
git clone https://github.com/Matheus0605/ecommerce-etl.git
cd ecommerce-etl
```

2. Crie e ative um virtualenv (Windows):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Instale dependências:

```bash
pip install -r requirements.txt
```

4. Gere dados (padrão: 10k customers, 50k products, 1M orders). Para smoke tests, reduza com variáveis de ambiente:

```powershell
# Exemplo (Windows PowerShell) — gera 1k / 5k / 10k
$env:CUSTOMER_QTY='1000'; $env:PRODUCT_QTY='5000'; $env:ORDER_QTY='10000'; .venv\Scripts\python.exe -m src.generators.generate_data
```

Os CSVs de entrada serão gravados em `data/raw/`.

---

## Rodando com Docker Compose

Há um setup docker-compose que cria um Postgres e o container da aplicação (Streamlit) para facilitar testes locais.

Credenciais (dev):
- POSTGRES_USER: postgres
- POSTGRES_PASSWORD: postgres
- POSTGRES_DB: etl_dw

Subir o ambiente:

```bash
# Em sistemas modernos com o plugin docker-compose use:
docker compose up --build
# Ou, se seu sistema tiver o wrapper antigo:
docker-compose up --build
```

- Streamlit (dashboard) ficará exposto em `http://127.0.0.1:8501`.
- O volume `./data` é montado no container para que Parquet/metrics fiquem acessíveis localmente.

> Nota: no Windows, se `http://localhost:8501` não abrir, tente `http://127.0.0.1:8501` — há diferenças de resolução de IPv6/IPv4 em alguns ambientes.

---

## Executando o pipeline

Existem duas formas principais:

1. Execução simples (sequencial / dev):

```bash
python -m src.pipeline.flow
```

O código aceita rodar mesmo quando o Postgres não estiver disponível — nesse caso o pipeline escreve arquivos Parquet em `data/silver/` e gera `data/metrics/quality_metrics.json`.

2. Com Prefect (orquestrador):

- O módulo `src/pipeline/flow.py` usa Prefect quando disponível. Para ambientes com Prefect Server/Cloud, registre o flow conforme sua infraestrutura.

---

## Camadas Silver / Gold

- Silver: arquivos Parquet em `data/silver/` (customers.parquet, products.parquet, orders.parquet). São artefatos enriquecidos e validados, prontos para consumo analítico.
- Gold: modelo dimensional carregado em Postgres (tabelas `dim_customers`, `dim_products`, `fact_orders`).

Observações:
- A carga para Postgres atualmente usa um wrapper `load_dataframe` baseado em `pandas.to_sql` para simplicidade. Para produção recomenda-se usar `COPY FROM` ou loaders em massa.
- Dimensional model definido em `src/models/dim_models.py` e criado via SQLAlchemy (função `create_all_tables`).

---

## Dashboard

Um dashboard simples em Streamlit (`src/dashboard/quality_dashboard.py`) lê `data/metrics/quality_metrics.json` e exibe métricas de qualidade do último run.

Executar localmente:

```bash
# preferível rodar via streamlit
streamlit run src/dashboard/quality_dashboard.py --server.address 127.0.0.1
```

Problemas comuns:
- Se `localhost:8501` não abrir, tente `127.0.0.1:8501`.

---

## CI / Tests

- Workflow GitHub Actions em `.github/workflows/ci.yml` roda `pytest` e constrói a imagem Docker (sem push). 
- Para rodar os testes localmente:

```bash
python -m pytest -q
```

---

## Estrutura do projeto

```
├── data/                       # raw, silver, gold artifacts (gerados)
├── src/
│   ├── extract/                # leitores (CSV)
│   ├── generators/             # geradores de dados e injeção de erros
│   ├── profiling/              # scripts de profiling e data quality
│   ├── transform/              # transformers por entidade
│   ├── pipeline/               # flow / pipeline orchestration
│   ├── load/                   # loaders (Postgres helper)
│   └── utils/                  # logging, config
├── tests/                      # pytest
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Como contribuir

1. Abra uma issue descrevendo a proposta.
2. Crie uma branch com um nome descritivo.
3. Submeta um Pull Request com testes e documentação.

Siga as práticas padrão de GitHub: commits pequenos, PRs atômicos e mensagens claras.

---

## Licença

Este projeto está aberto para uso educacional. Adicione aqui a licença desejada (por exemplo MIT) se quiser publicar.

---

## Autor

Matheus Pinheiro — https://github.com/Matheus0605

