import pandas as pd
import pytest

from src.analise import carregar_dados, calcular_indicadores


def criar_csv(tmp_path, conteudo):
    arquivo = tmp_path / "transacoes.csv"
    arquivo.write_text(conteudo, encoding="utf-8")
    return arquivo


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
    assert taxa == pytest.approx((1000 / 1500) * 100)


def test_calcular_indicadores_sem_receita():
    df = pd.DataFrame({"tipo": ["Despesa"], "valor": [100.0]})

    receitas, despesas, saldo, taxa = calcular_indicadores(df)

    assert receitas == 0.0
    assert despesas == 100.0
    assert saldo == -100.0
    assert taxa == 0.0


def test_carregar_dados_valida_e_cria_coluna_mes(tmp_path):
    arquivo = criar_csv(
        tmp_path,
        "id,data,categoria,tipo,descricao,valor,forma_pagamento\n"
        "1,2026-01-03,Alimentação,Despesa,Supermercado,120.50,Pix\n",
    )

    df = carregar_dados(arquivo)

    assert len(df) == 1
    assert df.loc[0, "mes"] == "2026-01"
    assert df.loc[0, "valor"] == 120.50
    assert pd.api.types.is_datetime64_any_dtype(df["data"])


def test_carregar_dados_rejeita_coluna_ausente(tmp_path):
    arquivo = criar_csv(tmp_path, "id,data,tipo,valor\n1,2026-01-03,Receita,100\n")

    with pytest.raises(ValueError, match="Colunas obrigatórias ausentes"):
        carregar_dados(arquivo)


def test_carregar_dados_rejeita_tipo_invalido(tmp_path):
    arquivo = criar_csv(
        tmp_path,
        "id,data,categoria,tipo,descricao,valor,forma_pagamento\n"
        "1,2026-01-03,Alimentação,Investimento,Aplicação,100,Pix\n",
    )

    with pytest.raises(ValueError, match="Tipos de transação inválidos"):
        carregar_dados(arquivo)


def test_carregar_dados_rejeita_valor_negativo(tmp_path):
    arquivo = criar_csv(
        tmp_path,
        "id,data,categoria,tipo,descricao,valor,forma_pagamento\n"
        "1,2026-01-03,Alimentação,Despesa,Compra,-10,Pix\n",
    )

    with pytest.raises(ValueError, match="não pode conter valores negativos"):
        carregar_dados(arquivo)


def test_carregar_dados_rejeita_data_invalida(tmp_path):
    arquivo = criar_csv(
        tmp_path,
        "id,data,categoria,tipo,descricao,valor,forma_pagamento\n"
        "1,data-invalida,Alimentação,Despesa,Compra,10,Pix\n",
    )

    with pytest.raises(ValueError, match="Datas inválidas"):
        carregar_dados(arquivo)


def test_carregar_dados_rejeita_ids_duplicados(tmp_path):
    arquivo = criar_csv(
        tmp_path,
        "id,data,categoria,tipo,descricao,valor,forma_pagamento\n"
        "1,2026-01-03,Alimentação,Despesa,Compra,10,Pix\n"
        "1,2026-01-04,Alimentação,Despesa,Outra compra,20,Pix\n",
    )

    with pytest.raises(ValueError, match="duplicados"):
        carregar_dados(arquivo)


def test_carregar_dados_rejeita_campo_textual_vazio(tmp_path):
    arquivo = criar_csv(
        tmp_path,
        "id,data,categoria,tipo,descricao,valor,forma_pagamento\n"
        "1,2026-01-03,,Despesa,Compra,10,Pix\n",
    )

    with pytest.raises(ValueError, match="ausentes ou vazios"):
        carregar_dados(arquivo)


def test_carregar_dados_rejeita_arquivo_vazio(tmp_path):
    arquivo = criar_csv(
        tmp_path,
        "id,data,categoria,tipo,descricao,valor,forma_pagamento\n",
    )

    with pytest.raises(ValueError, match="não contém transações"):
        carregar_dados(arquivo)
