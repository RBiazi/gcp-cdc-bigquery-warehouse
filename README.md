# Arquitetura de Dados — Pipeline OLTP (PostgreSQL) para Data Lake / Analytics

Projeto de portfólio de arquitetura de dados simulando um fluxo transacional (**OLTP**) até camadas analíticas estruturadas (**Bronze** e **Gold**) em ambiente local com armazenamento em **Google Drive**, sem custo em nuvem paga.

## Arquitetura Planejada
- **Origem OLTP:** PostgreSQL (`vendas_oltp`) com tabelas `clientes`, `produtos` e `pedidos`.
- **Camada Bronze:** Extrações brutas/snapshots salvos na pasta `data-lake-portfolio-bronze` no Google Drive.
- **Camada Gold:** Dados tratados e modelados para análise/BI na pasta `data-lake-portfolio-gold` no Google Drive.
- **Orquestração e BI:** Apache Airflow e Power BI.

## Estrutura do Projeto
- `sql/01_postgres_oltp.sql`: Script DDL e carga inicial do banco transacional
- `airflow/`: DAGs e configurações de orquestração
- `docs/prints/`: Evidências visuais das etapas do pipeline
- `README.md`: Documentação principal do projeto
