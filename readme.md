# Projeto de ETL: Análise de Dados do Setor Elétrico Brasileiro (ANEEL)

## Visão Geral

Este projeto consiste no desenvolvimento de um fluxo de trabalho de **Extração, Transformação e Carga (ETL)** completo, projetado para processar e analisar dados públicos da **Agência Nacional de Energia Elétrica (ANEEL)**. O objetivo principal é criar um Data Warehouse ou Data Mart que possibilite a realização de análises sobre o setor elétrico brasileiro, servindo como base para a disciplina de Gerenciamento de Banco de Dados da **Universidade Federal do Espírito Santo (UFES)**.

## Contexto do Projeto

Este trabalho acadêmico visa aplicar conceitos práticos de modelagem de dados, integração de dados e automação de processos em um cenário real. A ANEEL, como órgão regulador do setor elétrico no Brasil, disponibiliza uma vasta gama de dados abertos que são de grande relevância para a sociedade, pesquisadores e empresas. Este projeto busca explorar esse recurso, transformando dados brutos em informações estruturadas e prontas para análise.

## Fonte de Dados

Os dados utilizados neste projeto são provenientes do [Portal de Dados Abertos da ANEEL](https://dadosabertos.aneel.gov.br/). Dentre os diversos conjuntos de dados disponíveis, este projeto pode focar em temas como:

  * **Geração de Energia:** Informações sobre usinas, capacidade instalada, fontes de energia, etc.
  * **Distribuição de Energia:** Dados sobre interrupções no fornecimento, qualidade do serviço, tarifas, etc.

Os dados são disponibilizados em formatos como CSV, JSON e XML. A escolha do(s) conjunto(s) de dados específico(s) dependerá do escopo da análise a ser realizada.

## Arquitetura do ETL

O fluxo de ETL foi desenhado para ser modular e escalável. As principais etapas são:

1.  **Extração (Extract):** Scripts automatizados para baixar os conjuntos de dados mais recentes do portal da ANEEL.
2.  **Transformação (Transform):**
      * Limpeza e padronização dos dados (tratamento de valores nulos, correção de tipos de dados, etc.).
      * Enriquecimento dos dados (cruzamento com outras fontes de dados, se necessário).
      * Aplicação de regras de negócio.
      * Modelagem dos dados para um esquema dimensional (Star Schema ou Snowflake Schema).
3.  **Carga (Load):** Carregamento dos dados transformados em um banco de dados de destino (Data Warehouse ou Data Mart).

## Tecnologias Utilizadas

  * **Linguagem de Programação:** Python
      * **Bibliotecas:** Pandas, Requests, etc.
  * **Banco de Dados:** (PostgreSQL, MongoDB)
  * **Ferramentas de Orquestração (Opcional):** Apache Airflow.
  * **Ferramentas de Visualização (Opcional):** Power BI.

## Estrutura do Repositório

```
.
├── dag/
│   ├── stage/
│   └── dw/
├── etl/
│   ├── stage/
│   └── dw/
├── docs/
│   └── docker
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── .gitignore
└── README.md
```

## Autores

  * [Lucas Sobral](https://github.com/LTSobral)

## Agradecimentos

  * À **ANEEL** pela disponibilização dos dados abertos.
  * Ao Professor(a) da disciplina de Gerenciamento de Banco de Dados da **UFES** pelas orientações.