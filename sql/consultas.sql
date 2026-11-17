-- Consultas SQL do projeto
-- Banco: SQLite
-- Tabela: transacoes
-- Execute as consultas individualmente no SQLite.

-- 1. Total de receitas
SELECT ROUND(COALESCE(SUM(valor), 0), 2) AS total_receitas
FROM transacoes
WHERE tipo = 'Receita';

-- 2. Total de despesas
SELECT ROUND(COALESCE(SUM(valor), 0), 2) AS total_despesas
FROM transacoes
WHERE tipo = 'Despesa';

-- 3. Saldo geral
SELECT ROUND(
    SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE -valor END),
    2
) AS saldo
FROM transacoes;

-- 4. Despesas por categoria e participação no total
WITH totais AS (
    SELECT categoria, SUM(valor) AS total_categoria
    FROM transacoes
    WHERE tipo = 'Despesa'
    GROUP BY categoria
)
SELECT
    categoria,
    ROUND(total_categoria, 2) AS total_despesas,
    ROUND(
        total_categoria * 100.0 / NULLIF(SUM(total_categoria) OVER (), 0),
        2
    ) AS participacao_percentual
FROM totais
ORDER BY total_despesas DESC;

-- 5. Receitas por categoria
SELECT
    categoria,
    ROUND(SUM(valor), 2) AS total_receitas
FROM transacoes
WHERE tipo = 'Receita'
GROUP BY categoria
ORDER BY total_receitas DESC;

-- 6. Resumo mensal: receitas, despesas e saldo
SELECT
    strftime('%Y-%m', data) AS mes,
    ROUND(SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE 0 END), 2) AS receitas,
    ROUND(SUM(CASE WHEN tipo = 'Despesa' THEN valor ELSE 0 END), 2) AS despesas,
    ROUND(SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE -valor END), 2) AS saldo
FROM transacoes
GROUP BY strftime('%Y-%m', data)
ORDER BY mes;

-- 7. Taxa de poupança mensal
WITH resumo AS (
    SELECT
        strftime('%Y-%m', data) AS mes,
        SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE 0 END) AS receitas,
        SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE -valor END) AS saldo
    FROM transacoes
    GROUP BY strftime('%Y-%m', data)
)
SELECT
    mes,
    ROUND(receitas, 2) AS receitas,
    ROUND(saldo, 2) AS saldo,
    ROUND(saldo * 100.0 / NULLIF(receitas, 0), 2) AS taxa_poupanca_percentual
FROM resumo
ORDER BY mes;

-- 8. Cinco maiores despesas
SELECT
    data,
    descricao,
    categoria,
    ROUND(valor, 2) AS valor
FROM transacoes
WHERE tipo = 'Despesa'
ORDER BY valor DESC
LIMIT 5;

-- 9. Despesas por forma de pagamento
SELECT
    forma_pagamento,
    ROUND(SUM(valor), 2) AS total_despesas
FROM transacoes
WHERE tipo = 'Despesa'
GROUP BY forma_pagamento
ORDER BY total_despesas DESC;

-- 10. Variação das despesas em relação ao mês anterior
WITH despesas_mensais AS (
    SELECT
        strftime('%Y-%m', data) AS mes,
        SUM(valor) AS total_despesas
    FROM transacoes
    WHERE tipo = 'Despesa'
    GROUP BY strftime('%Y-%m', data)
),
comparativo AS (
    SELECT
        mes,
        total_despesas,
        LAG(total_despesas) OVER (ORDER BY mes) AS despesas_mes_anterior
    FROM despesas_mensais
)
SELECT
    mes,
    ROUND(total_despesas, 2) AS despesas,
    ROUND(despesas_mes_anterior, 2) AS despesas_mes_anterior,
    ROUND(
        (total_despesas - despesas_mes_anterior) * 100.0
        / NULLIF(despesas_mes_anterior, 0),
        2
    ) AS variacao_percentual
FROM comparativo
ORDER BY mes;

-- 11. Quantidade de transações e valor médio por categoria
SELECT
    categoria,
    COUNT(*) AS quantidade_transacoes,
    ROUND(AVG(valor), 2) AS valor_medio
FROM transacoes
WHERE tipo = 'Despesa'
GROUP BY categoria
ORDER BY quantidade_transacoes DESC, valor_medio DESC;

-- 12. Histórico completo de transações
SELECT
    date(data) AS data,
    tipo,
    categoria,
    descricao,
    ROUND(valor, 2) AS valor,
    forma_pagamento
FROM transacoes
ORDER BY date(data), id;
