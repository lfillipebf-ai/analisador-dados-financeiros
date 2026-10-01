from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "transacoes.csv"
OUTPUT_DIR = BASE_DIR / "output"
DB_FILE = OUTPUT_DIR / "financeiro.db"

def carregar_dados():
    df = pd.read_csv(DATA_FILE, parse_dates=["data"])
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["mes"] = df["data"].dt.to_period("M").astype(str)
    return df.dropna(subset=["valor"])

def calcular_indicadores(df):
    receitas = df.loc[df["tipo"] == "Receita", "valor"].sum()
    despesas = df.loc[df["tipo"] == "Despesa", "valor"].sum()
    saldo = receitas - despesas
    taxa_poupanca = (saldo / receitas * 100) if receitas else 0
    return receitas, despesas, saldo, taxa_poupanca

def salvar_sqlite(df):
    conn = sqlite3.connect(DB_FILE)
    df.to_sql("transacoes", conn, if_exists="replace", index=False)
    conn.close()

def gerar_graficos(df):
    despesas = df[df["tipo"] == "Despesa"].groupby("categoria")["valor"].sum().sort_values(ascending=False)
    ax = despesas.plot(kind="bar", title="Despesas por categoria")
    ax.set_ylabel("Valor (R$)")
    ax.set_xlabel("Categoria")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "despesas_por_categoria.png", dpi=150)
    plt.close()

    mensal = df.groupby(["mes", "tipo"])["valor"].sum().unstack(fill_value=0)
    ax = mensal.plot(kind="bar", title="Receitas x Despesas por mês")
    ax.set_ylabel("Valor (R$)")
    ax.set_xlabel("Mês")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "evolucao_mensal.png", dpi=150)
    plt.close()

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = carregar_dados()
    receitas, despesas, saldo, taxa = calcular_indicadores(df)
    salvar_sqlite(df)
    gerar_graficos(df)

    resumo = pd.DataFrame({
        "indicador": ["Total de receitas", "Total de despesas", "Saldo", "Taxa de poupança"],
        "valor": [receitas, despesas, saldo, taxa]
    })
    resumo.to_csv(OUTPUT_DIR / "resumo.csv", index=False)

    print("=== RESUMO FINANCEIRO ===")
    print(f"Receitas: R$ {receitas:,.2f}")
    print(f"Despesas: R$ {despesas:,.2f}")
    print(f"Saldo: R$ {saldo:,.2f}")
    print(f"Taxa de poupança: {taxa:.2f}%")
    print("\nArquivos gerados em:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
