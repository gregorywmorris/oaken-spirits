SELECT
    c.CategoryName,
    s.SaleDate,
    SUM(s.SaleDollars) AS TotalSalesDollars,
    SUM(s.BottlesSold) AS TotalBottlesSold
FROM {{ ref('stg_sales') }} s
JOIN {{ ref('stg_product') }} p ON s.ItemNumber = p.ItemNumber
JOIN {{ ref('stg_category') }} c ON p.CategoryNumber = c.CategoryNumber
GROUP BY c.CategoryName, s.SaleDate
ORDER BY SaleDate DESC
