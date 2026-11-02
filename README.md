# Analisador de Dados Financeiros

Projeto de portfólio e estudo desenvolvido em **Python** para transformar transações financeiras fictícias em indicadores, consultas SQL e visualizações.

## Objetivo

Praticar um fluxo completo de análise de dados:

- leitura e validação de dados CSV;
- tratamento de valores e datas com Pandas;
- cálculo de receitas, despesas, saldo e taxa de poupança;
- consultas SQL com SQLite;
- geração de gráficos com Matplotlib;
- exportação de resultados em CSV;
- testes automatizados com Pytest;
- execução automática de validações pelo GitHub Actions.

## Tecnologias

- Python 3.11+
- Pandas
- Matplotlib
- SQLite
- SQL
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

Os arquivos gerados pela execução ficam em `output/` e não são versionados.

## Como executar

### 1. Clonar o projeto

```bash
git clone https://github.com/lfillipebf-ai/analisador-dados-financeiros.git
cd analisador-dados-financeiros
```

### 2. Criar ambiente virtual

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

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a análise

```bash
python src/analise.py
```

A execução cria:

- `output/financeiro.db` — banco SQLite;
- `output/resumo.csv` — indicadores calculados;
- `output/despesas_por_categoria.png` — gráfico de despesas;
- `output/evolucao_mensal.png` — gráfico mensal.

### 5. Executar os testes

```bash
pytest
```

## SQL

O arquivo `sql/consultas.sql` contém consultas para totais, saldo, despesas por categoria, receitas por categoria, evolução mensal, maiores despesas e formas de pagamento.

## Dados

Os dados de `data/transacoes.csv` são **fictícios** e foram criados exclusivamente para fins educacionais e de portfólio. Não representam dados financeiros reais.

## Autor

**Luis Fillipe Backer Faria**

GitHub: https://github.com/lfillipebf-ai
