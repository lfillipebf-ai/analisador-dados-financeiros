from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "transacoes.csv"
OUTPUT_DIR = BASE_DIR / "output"
DB_FILE = OUTPUT_DIR / "financeiro.db"

COLUNAS_OBRIGATORIAS = {
    "id",
    "data",
    "categoria",
    "tipo",
    "descricao",
    "valor",
    "forma_pagamento",
}
TIPOS_VALIDOS = {"Receita", "Despesa"}


def carregar_dados(data_file: Path = DATA_FILE) -> pd.DataFrame:
    """Carrega e valida as transações financeiras antes da análise."""
    df = pd.read_csv(data_file)

    missing = COLUNAS_OBRIGATORIAS - set(df.columns)
    if missing:
        raise ValueError(
            f"Colunas obrigatórias ausentes: {', '.join(sorted(missing))}"
        )

    if df.empty:
        raise ValueError("O arquivo não contém transações.")

    campos_texto = ["categoria", "tipo", "descricao", "forma_pagamento"]
    for coluna in campos_texto:
        df[coluna] = df[coluna].astype("string").str.strip()
        invalidos = df[coluna].isna() | df[coluna].eq("")
        if invalidos.any():
            linhas = (df.index[invalidos] + 2).tolist()
            raise ValueError(
                f"Valores ausentes ou vazios na coluna '{coluna}' "
                f"(linhas do CSV: {linhas})."
            )

    ids = pd.to_numeric(df["id"], errors="coerce")
    if ids.isna().any() or (ids % 1 != 0).any():
        raise ValueError("A coluna 'id' deve conter apenas números inteiros.")
    if ids.duplicated().any():
        raise ValueError("A coluna 'id' não pode conter valores duplicados.")
    df["id"] = ids.astype("int64")

    datas = pd.to_datetime(df["data"], errors="coerce")
    if datas.isna().any():
        linhas = (df.index[datas.isna()] + 2).tolist()
        raise ValueError(f"Datas inválidas no CSV (linhas: {linhas}).")
    df["data"] = datas

    valores = pd.to_numeric(df["valor"], errors="coerce")
    if valores.isna().any():
        linhas = (df.index[valores.isna()] + 2).tolist()
        raise ValueError(f"Valores monetários inválidos no CSV (linhas: {linhas}).")
    if (valores < 0).any():
        raise ValueError("A coluna 'valor' não pode conter valores negativos.")
    df["valor"] = valores.astype(float)

    tipos_invalidos = sorted(set(df["tipo"].unique()) - TIPOS_VALIDOS)
    if tipos_invalidos:
        raise ValueError(f"Tipos de transação inválidos: {tipos_invalidos}")

    df["mes"] = df["data"].dt.to_period("M").astype(str)
    return df


def calcular_indicadores(df: pd.DataFrame) -> tuple[float, float, float, float]:
    """Calcula receitas, despesas, saldo e taxa de poupança."""
    receitas = float(df.loc[df["tipo"] == "Receita", "valor"].sum())
    despesas = float(df.loc[df["tipo"] == "Despesa", "valor"].sum())
    saldo = receitas - despesas
    taxa_poupanca = (saldo / receitas * 100) if receitas else 0.0
    return receitas, despesas, saldo, float(taxa_poupanca)


def salvar_sqlite(df: pd.DataFrame, db_file: Path = DB_FILE) -> None:
    """Salva as transações em um banco SQLite."""
    db_file.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_file) as conn:
        df.to_sql("transacoes", conn, if_exists="replace", index=False)


def gerar_graficos(df: pd.DataFrame, output_dir: Path = OUTPUT_DIR) -> None:
    """Gera gráficos de despesas por categoria e evolução mensal."""
    output_dir.mkdir(parents=True, exist_ok=True)

    despesas = (
        df[df["tipo"] == "Despesa"]
        .groupby("categoria")["valor"]
        .sum()
        .sort_values(ascending=False)
    )
    ax = despesas.plot(kind="bar", title="Despesas por categoria")
    ax.set_ylabel("Valor (R$)")
    ax.set_xlabel("Categoria")
    plt.tight_layout()
    plt.savefig(output_dir / "despesas_por_categoria.png", dpi=150)
    plt.close()

    mensal = df.groupby(["mes", "tipo"])["valor"].sum().unstack(fill_value=0)
    ax = mensal.plot(kind="bar", title="Receitas x Despesas por mês")
    ax.set_ylabel("Valor (R$)")
    ax.set_xlabel("Mês")
    plt.tight_layout()
    plt.savefig(output_dir / "evolucao_mensal.png", dpi=150)
    plt.close()


def salvar_resumo(
    receitas: float,
    despesas: float,
    saldo: float,
    taxa: float,
    output_dir: Path = OUTPUT_DIR,
) -> None:
    """Salva os principais indicadores em CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)
    resumo = pd.DataFrame(
        {
            "indicador": [
                "Total de receitas",
                "Total de despesas",
                "Saldo",
                "Taxa de poupança",
            ],
            "valor": [receitas, despesas, saldo, taxa],
        }
    )
    resumo.to_csv(output_dir / "resumo.csv", index=False)


def main() -> None:
    df = carregar_dados()
    receitas, despesas, saldo, taxa = calcular_indicadores(df)
    salvar_sqlite(df)
    gerar_graficos(df)
    salvar_resumo(receitas, despesas, saldo, taxa)

    print("=== RESUMO FINANCEIRO ===")
    print(f"Receitas: R$ {receitas:,.2f}")
    print(f"Despesas: R$ {despesas:,.2f}")
    print(f"Saldo: R$ {saldo:,.2f}")
    print(f"Taxa de poupança: {taxa:.2f}%")
    print(f"\nArquivos gerados em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
