# Analisador de Dados Financeiros

Projeto de portfólio desenvolvido em **Python** para transformar transações financeiras fictícias em indicadores, consultas SQL e visualizações.

## Objetivo

Praticar um fluxo de análise de dados com:

- leitura e validação de dados CSV;
- tratamento de valores e datas com Pandas;
- cálculo de receitas, despesas, saldo e taxa de poupança;
- análise mensal de receitas, despesas, saldo e taxa de poupança;
- persistência dos dados em SQLite;
- consultas SQL com agregações, CTEs e funções de janela;
- geração de gráficos com Matplotlib;
- exportação de indicadores gerais e mensais em CSV;
- testes automatizados com Pytest;
- integração contínua com GitHub Actions.

## Tecnologias

- Python 3.11+
- Pandas
- Matplotlib
- SQLite e SQL
- Jupyter Notebook
- Pytest
- GitHub Actions

## Estrutura

```text
analisador-dados-financeiros/
├── data/
│   └── transacoes.csv
├── notebooks/
│   └── analise_financeira.ipynb
├── sql/
│   └── consultas.sql
├── src/
│   └── analise.py
├── tests/
│   ├── test_analise.py
│   └── test_consultas_sql.py
├── .github/workflows/
│   └── ci.yml
├── requirements.txt
└── README.md
```

Os arquivos gerados ficam em `output/`, diretório que não é versionado.

## Como executar

### 1. Clonar o projeto

```bash
git clone https://github.com/lfillipebf-ai/analisador-dados-financeiros.git
cd analisador-dados-financeiros
```

### 2. Criar e ativar o ambiente virtual

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### Abrir o notebook

Na raiz do projeto, execute:

```bash
jupyter notebook notebooks/analise_financeira.ipynb
```

O notebook localiza o CSV tanto quando iniciado pela raiz quanto pela pasta `notebooks/`.

### 4. Executar a análise

```bash
python src/analise.py
```

A execução gera:

- `output/financeiro.db` — banco de dados SQLite;
- `output/resumo.csv` — indicadores financeiros gerais;
- `output/resumo_mensal.csv` — receitas, despesas, saldo e taxa de poupança por mês;
- `output/despesas_por_categoria.png` — despesas por categoria em gráfico horizontal;
- `output/evolucao_mensal.png` — comparação mensal entre receitas e despesas;
- `output/saldo_mensal.png` — evolução do saldo ao longo dos meses.

### 5. Consultar o banco e executar SQL

Depois de executar a análise, o banco SQLite estará em `output/financeiro.db`. Abra esse arquivo em uma ferramenta compatível com SQLite e execute individualmente as instruções de `sql/consultas.sql`.

### 6. Executar os testes

```bash
pytest -v
```

Os testes verificam os cálculos gerais e mensais, a criação dos três gráficos, a validação dos dados de entrada, a persistência no SQLite e os resultados esperados das consultas SQL.

## Exemplo de resultados

Com os 30 registros fictícios incluídos no CSV, os indicadores gerais são:

| Indicador | Resultado |
|---|---:|
| Receitas | R$ 14.900,00 |
| Despesas | R$ 6.583,70 |
| Saldo | R$ 8.316,30 |
| Taxa de poupança | 55,81% |

Resumo mensal:

| Mês | Receitas | Despesas | Saldo |
|---|---:|---:|---:|
| 2026-01 | R$ 4.850,00 | R$ 2.130,10 | R$ 2.719,90 |
| 2026-02 | R$ 5.100,00 | R$ 2.185,30 | R$ 2.914,70 |
| 2026-03 | R$ 4.950,00 | R$ 2.268,30 | R$ 2.681,70 |

Esses valores são reproduzíveis a partir do arquivo de dados do repositório e não representam movimentações financeiras reais.

## Consultas SQL

O arquivo `sql/consultas.sql` reúne 12 consultas para SQLite:

1. Total de receitas.
2. Total de despesas.
3. Saldo geral.
4. Despesas por categoria e participação percentual no total.
5. Receitas por categoria.
6. Resumo mensal com receitas, despesas e saldo.
7. Taxa de poupança mensal.
8. Cinco maiores despesas.
9. Despesas por forma de pagamento.
10. Variação percentual das despesas em relação ao mês anterior.
11. Quantidade de transações e valor médio por categoria.
12. Histórico completo de transações, ordenado por data.

As consultas demonstram o uso de `GROUP BY`, agregações, CTEs (`WITH`), `NULLIF`, `LAG` e funções de janela. Execute cada consulta individualmente no SQLite.

## Estrutura dos dados

O arquivo `data/transacoes.csv` contém as seguintes colunas:

| Coluna | Descrição |
|---|---|
| `id` | Identificador inteiro e único da transação |
| `data` | Data da movimentação no formato ISO |
| `categoria` | Categoria financeira |
| `tipo` | Natureza da movimentação: Receita ou Despesa |
| `descricao` | Descrição da transação |
| `valor` | Valor numérico não negativo em reais |
| `forma_pagamento` | Meio utilizado na movimentação |

A coluna `mes` é derivada da data durante o processamento e não precisa existir no CSV original.

## Dados

Os registros de `data/transacoes.csv` são **fictícios**, criados exclusivamente para fins educacionais e de portfólio. Não representam dados financeiros reais.

## Autor

**Luis Fillipe Backer Faria**

- GitHub: https://github.com/lfillipebf-ai
- Repositório: https://github.com/lfillipebf-ai/analisador-dados-financeiros
