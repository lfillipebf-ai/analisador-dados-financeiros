import pandas as pd

from src.analise import calcular_indicadores


def test_calcular_indicadores():
    df = pd.DataFrame(
        {
            "tipo": ["Receita", "Receita", "Despesa", "Despesa"],
            "valor": [1000.0, 500.0, 300.0, 200.0],
        }
    )

    receitas, despesas, saldo, taxa = calcular_indicadores(df)

    assert receitas == 1500.0
    assert despesas == 500.0
    assert saldo == 1000.0
    assert taxa == (1000 / 1500) * 100


def test_calcular_indicadores_sem_receita():
    df = pd.DataFrame({"tipo": ["Despesa"], "valor": [100.0]})

    receitas, despesas, saldo, taxa = calcular_indicadores(df)

    assert receitas == 0.0
    assert despesas == 100.0
    assert saldo == -100.0
    assert taxa == 0.0
