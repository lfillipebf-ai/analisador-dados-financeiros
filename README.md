# Analisador de Dados Financeiros

Projeto de portfólio desenvolvido em **Python** para transformar transações financeiras fictícias em indicadores, consultas SQL e visualizações.

## Objetivo

Praticar um fluxo de análise de dados com:

- leitura e validação de dados CSV;
- tratamento de valores e datas com Pandas;
- cálculo de receitas, despesas, saldo e taxa de poupança;
- análise mensal de receitas, despesas, saldo e taxa de poupança;
- persistência dos dados em SQLite;
- consultas SQL;
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
│   └── test_analise.py
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
.venv\\Scripts\\activate
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

### 5. Executar os testes

```bash
pytest -v
```

Os testes verificam os cálculos gerais e mensais, a criação dos três gráficos e a validação de arquivos CSV, incluindo colunas ausentes, datas inválidas, valores negativos, tipos desconhecidos, IDs duplicados e campos vazios.

## Consultas SQL

O arquivo `sql/consultas.sql` contém exemplos de consultas para totais, saldo, despesas e receitas por categoria, evolução mensal, maiores despesas e formas de pagamento.

## Dados

Os registros de `data/transacoes.csv` são **fictícios**, criados exclusivamente para fins educacionais e de portfólio. Não representam dados financeiros reais.

## Autor

**Luis Fillipe Backer Faria**

- GitHub: https://github.com/lfillipebf-ai
- Repositório: https://github.com/lfillipebf-ai/analisador-dados-financeiros
