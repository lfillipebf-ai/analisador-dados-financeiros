-- Consultas SQL do projeto
-- Banco: SQLite

SELECT ROUND(SUM(valor), 2) AS total_receitas FROM transacoes WHERE tipo = 'Receita';

SELECT ROUND(SUM(valor), 2) AS total_despesas FROM transacoes WHERE tipo = 'Despesa';

SELECT ROUND(SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE -valor END), 2) AS saldo
FROM transacoes;

SELECT categoria, ROUND(SUM(valor), 2) AS total
FROM transacoes WHERE tipo = 'Despesa'
GROUP BY categoria ORDER BY total DESC;

SELECT categoria, ROUND(SUM(valor), 2) AS total
FROM transacoes WHERE tipo = 'Receita'
GROUP BY categoria ORDER BY total DESC;

SELECT strftime('%Y-%m', data) AS mes,
       ROUND(SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE 0 END), 2) AS receitas,
       ROUND(SUM(CASE WHEN tipo = 'Despesa' THEN valor ELSE 0 END), 2) AS despesas
FROM transacoes GROUP BY mes ORDER BY mes;

SELECT descricao, categoria, valor
FROM transacoes WHERE tipo = 'Despesa'
ORDER BY valor DESC LIMIT 5;

SELECT forma_pagamento, ROUND(SUM(valor), 2) AS total
FROM transacoes WHERE tipo = 'Despesa'
GROUP BY forma_pagamento ORDER BY total DESC;
