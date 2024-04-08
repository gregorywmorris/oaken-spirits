WITH base AS (
  SELECT 
    ItemNumber,
    COUNT(ItemNumber) AS purchase_count
  FROM {{ ref('stg_sales') }}
  GROUP BY ItemNumber
),
product AS (
  SELECT
    ItemNumber,
    ItemDescription
  FROM {{ ref('stg_product') }}
)

SELECT 
  p.ItemNumber,
  p.ItemDescription,
  b.purchase_count
FROM {{ ref('stg_product') }} p
LEFT JOIN base b ON p.ItemNumber = b.ItemNumber
ORDER BY b.purchase_count DESC
