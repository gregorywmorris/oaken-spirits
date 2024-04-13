WITH base AS (
  SELECT
    p.ItemNumber,
    c.CategoryName,
    SUM(s.SaleDollars) AS TotalSalesDollars
  FROM {{ ref('stg_sales') }} s
  JOIN {{ ref('stg_product') }} p ON s.ItemNumber = p.ItemNumber
  JOIN {{ ref('stg_category') }} c ON p.CategoryNumber = c.CategoryNumber
  GROUP BY p.ItemNumber, c.CategoryName
  ORDER BY TotalSalesDollars DESC
  LIMIT 10
)
SELECT
    b.CategoryName,
    s.SaleDate,
    SUM(s.SaleDollars) AS TotalSalesDollars,
    SUM(s.BottlesSold) AS TotalBottlesSold
FROM {{ ref('stg_sales') }} s
JOIN base b ON s.ItemNumber = b.ItemNumber
LEFT JOIN {{ ref('stg_product') }}  p ON s.ItemNumber = p.ItemNumber
LEFT JOIN {{ ref('stg_category') }}  c ON p.CategoryNumber = c.CategoryNumber
GROUP BY b.CategoryName, s.SaleDate
ORDER BY s.SaleDate ASC