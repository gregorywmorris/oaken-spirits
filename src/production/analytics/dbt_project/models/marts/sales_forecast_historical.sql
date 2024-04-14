SELECT
    s.SaleDate,
    sum(s.SaleDollars) TotalSalesDollars
FROM {{ ref('stg_sales') }} s
GROUP BY SaleDate
ORDER BY s.SaleDate ASC