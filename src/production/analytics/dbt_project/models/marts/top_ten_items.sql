WITH base AS (
  SELECT
    p.ItemNumber,
    p.ItemDescription,
    SUM(s.SaleDollars) AS TotalSalesDollars
  FROM {{ ref('stg_sales') }} s
  JOIN {{ ref('stg_product') }} p ON s.ItemNumber = p.ItemNumber
  GROUP BY p.ItemNumber, p.ItemDescription
  ORDER BY TotalSalesDollars DESC
  LIMIT 10
)
SELECT
    p.ItemDescription,
    s.SaleDate,
    SUM(s.SaleDollars) AS TotalSalesDollars,
    SUM(s.BottlesSold) AS TotalBottlesSold
FROM {{ ref('stg_sales') }} s
JOIN base b ON s.ItemNumber = b.ItemNumber
LEFT JOIN {{ ref('stg_product') }}  p ON s.ItemNumber = p.ItemNumber
GROUP BY p.ItemDescription, s.SaleDate
ORDER BY s.SaleDate ASC