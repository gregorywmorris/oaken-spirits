SELECT
    sales.sale_date,
    sum(sales.sale_amount) total_sale_dollar
FROM {{ ref('stg_sales') }} sales
GROUP BY sale_date
ORDER BY sales.sale_date ASC