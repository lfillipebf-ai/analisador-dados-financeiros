import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "transacoes.csv"
SQL_FILE = BASE_DIR / "sql" / "consultas.sql"


def test_consultas_sql_executam_com_dados_do_projeto():
    dados = pd.read_csv(DATA_FILE)
    script = SQL_FILE.read_text(encoding="utf-8")

    with sqlite3.connect(":memory:") as conexao:
        dados.to_sql("transacoes", conexao, index=False)

        consulta_atual = ""
        quantidade_consultas = 0

        for linha in script.splitlines():
            consulta_atual += linha + "\n"

            if sqlite3.complete_statement(consulta_atual):
                if consulta_atual.strip():
                    conexao.execute(consulta_atual)
                    quantidade_consultas += 1
                consulta_atual = ""

        assert quantidade_consultas == 12
