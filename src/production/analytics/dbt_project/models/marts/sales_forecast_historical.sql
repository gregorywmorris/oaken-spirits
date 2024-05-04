SELECT
    s.sale_date,
    sum(s.sale_amount) total_sale_dollar
FROM {{ ref('stg_sales') }} s
GROUP BY sale_date
ORDER BY s.sale_date ASC