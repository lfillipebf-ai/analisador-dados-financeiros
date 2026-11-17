import sqlite3
from pathlib import Path

import pandas as pd
import pytest


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "transacoes.csv"
SQL_FILE = BASE_DIR / "sql" / "consultas.sql"


def test_consultas_sql_executam_e_retornam_resultados_esperados():
    dados = pd.read_csv(DATA_FILE)
    script = SQL_FILE.read_text(encoding="utf-8")

    with sqlite3.connect(":memory:") as conexao:
        dados.to_sql("transacoes", conexao, index=False)

        consulta_atual = ""
        resultados = []

        for linha in script.splitlines():
            consulta_atual += linha + "\n"

            if sqlite3.complete_statement(consulta_atual):
                if consulta_atual.strip():
                    cursor = conexao.execute(consulta_atual)
                    resultados.append(cursor.fetchall())
                consulta_atual = ""

        assert len(resultados) == 12

        assert resultados[0][0][0] == pytest.approx(14900.00)
        assert resultados[1][0][0] == pytest.approx(6583.70)
        assert resultados[2][0][0] == pytest.approx(8316.30)

        assert resultados[5] == [
            ("2026-01", 4850.0, 2130.1, 2719.9),
            ("2026-02", 5100.0, 2185.3, 2914.7),
            ("2026-03", 4950.0, 2268.3, 2681.7),
        ]

        assert len(resultados[11]) == 30
