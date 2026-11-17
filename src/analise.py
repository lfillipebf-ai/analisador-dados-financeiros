from decimal import Decimal, InvalidOperation
from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

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
    df = pd.read_csv(data_file, dtype="string")

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

    ids = []
    for valor_id in df["id"]:
        try:
            numero = Decimal(str(valor_id).strip())
        except (InvalidOperation, ValueError):
            raise ValueError(
                "A coluna 'id' deve conter apenas números inteiros válidos."
            ) from None

        if not numero.is_finite() or numero != numero.to_integral_value():
            raise ValueError(
                "A coluna 'id' deve conter apenas números inteiros válidos."
            )
        if numero < 0 or numero > Decimal(np.iinfo("int64").max):
            raise ValueError(
                "Os IDs devem estar dentro do intervalo de inteiros permitido."
            )
        ids.append(int(numero))

    if len(ids) != len(set(ids)):
        raise ValueError("A coluna 'id' não pode conter valores duplicados.")
    df["id"] = pd.Series(ids, index=df.index, dtype="int64")

    datas = pd.to_datetime(df["data"], errors="coerce")
    if datas.isna().any():
        linhas = (df.index[datas.isna()] + 2).tolist()
        raise ValueError(f"Datas inválidas no CSV (linhas: {linhas}).")
    df["data"] = datas

    valores = pd.to_numeric(df["valor"], errors="coerce")
    invalidos = valores.isna() | ~np.isfinite(valores)
    if invalidos.any():
        linhas = (df.index[invalidos] + 2).tolist()
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


def calcular_resumo_mensal(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula receitas, despesas, saldo e taxa de poupança por mês."""
    mensal = (
        df.pivot_table(
            index="mes",
            columns="tipo",
            values="valor",
            aggfunc="sum",
            fill_value=0,
        )
        .reindex(columns=["Receita", "Despesa"], fill_value=0)
        .sort_index()
    )

    resumo = pd.DataFrame(index=mensal.index)
    resumo["receitas"] = mensal["Receita"]
    resumo["despesas"] = mensal["Despesa"]
    resumo["saldo"] = resumo["receitas"] - resumo["despesas"]
    resumo["taxa_poupanca"] = (
        resumo["saldo"].div(resumo["receitas"].where(resumo["receitas"] != 0)) * 100
    ).fillna(0.0)
    resumo.index.name = "mes"
    return resumo.reset_index()


def salvar_sqlite(df: pd.DataFrame, db_file: Path = DB_FILE) -> None:
    """Salva as transações em um banco SQLite."""
    db_file.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_file) as conn:
        df.to_sql("transacoes", conn, if_exists="replace", index=False)


def formatar_reais(valor: float, _posicao: int) -> str:
    """Formata valores monetários para os eixos dos gráficos."""
    return f"R$ {valor:,.0f}".replace(",", ".")


def gerar_graficos(df: pd.DataFrame, output_dir: Path = OUTPUT_DIR) -> None:
    """Gera gráficos de despesas por categoria e evolução financeira mensal."""
    output_dir.mkdir(parents=True, exist_ok=True)
    formatador = FuncFormatter(formatar_reais)

    despesas = (
        df[df["tipo"] == "Despesa"]
        .groupby("categoria")["valor"]
        .sum()
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    if not despesas.empty:
        barras = ax.barh(despesas.index, despesas.values)
        ax.bar_label(
            barras,
            labels=[formatar_reais(v, 0) for v in despesas.values],
            padding=5,
            fontsize=9,
        )
    else:
        ax.text(
            0.5,
            0.5,
            "Nenhuma despesa registrada",
            ha="center",
            va="center",
            transform=ax.transAxes,
        )
    ax.set_title("Despesas por categoria", loc="left", fontsize=15, pad=14)
    ax.set_xlabel("Valor (R$)")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(formatador)
    ax.grid(axis="x", alpha=0.25)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(
        output_dir / "despesas_por_categoria.png",
        dpi=180,
        bbox_inches="tight",
    )
    plt.close(fig)

    mensal = (
        df.groupby(["mes", "tipo"])["valor"]
        .sum()
        .unstack(fill_value=0)
        .reindex(columns=["Receita", "Despesa"], fill_value=0)
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    mensal.plot(kind="bar", ax=ax, width=0.75)
    ax.set_title("Receitas x despesas por mês", loc="left", fontsize=15, pad=14)
    ax.set_xlabel("Mês")
    ax.set_ylabel("Valor (R$)")
    ax.yaxis.set_major_formatter(formatador)
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    ax.legend(title="Tipo", frameon=False)
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    fig.savefig(
        output_dir / "evolucao_mensal.png",
        dpi=180,
        bbox_inches="tight",
    )
    plt.close(fig)

    resumo = calcular_resumo_mensal(df).set_index("mes")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(resumo.index, resumo["saldo"], marker="o", linewidth=2)
    ax.axhline(0, linewidth=1, alpha=0.6)
    ax.set_title("Evolução do saldo mensal", loc="left", fontsize=15, pad=14)
    ax.set_xlabel("Mês")
    ax.set_ylabel("Saldo (R$)")
    ax.yaxis.set_major_formatter(formatador)
    ax.grid(axis="y", alpha=0.25)
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    fig.savefig(
        output_dir / "saldo_mensal.png",
        dpi=180,
        bbox_inches="tight",
    )
    plt.close(fig)


def salvar_resumo(
    receitas: float,
    despesas: float,
    saldo: float,
    taxa: float,
    output_dir: Path = OUTPUT_DIR,
) -> None:
    """Salva os principais indicadores gerais em CSV."""
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


def salvar_resumo_mensal(
    resumo_mensal: pd.DataFrame,
    output_dir: Path = OUTPUT_DIR,
) -> None:
    """Exporta os indicadores financeiros agrupados por mês."""
    output_dir.mkdir(parents=True, exist_ok=True)
    resumo_mensal.to_csv(output_dir / "resumo_mensal.csv", index=False)


def main() -> None:
    df = carregar_dados()
    receitas, despesas, saldo, taxa = calcular_indicadores(df)
    resumo_mensal = calcular_resumo_mensal(df)

    salvar_sqlite(df)
    gerar_graficos(df)
    salvar_resumo(receitas, despesas, saldo, taxa)
    salvar_resumo_mensal(resumo_mensal)

    print("=== RESUMO FINANCEIRO ===")
    print(f"Receitas: R$ {receitas:,.2f}")
    print(f"Despesas: R$ {despesas:,.2f}")
    print(f"Saldo: R$ {saldo:,.2f}")
    print(f"Taxa de poupança: {taxa:.2f}%")
    print(f"\nArquivos gerados em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
