WITH base AS (
  SELECT 
    ItemNumber,
    COUNT(ItemNumber) AS purchase_count
  FROM {{ ref('stg_sales') }}
  GROUP BY 1
)

SELECT 
  p.ItemNumber,
  p.ItemName,
  p.ItemDescription,
  b.purchase_count
FROM {{ ref('stg_product') }} p
LEFT JOIN base b ON p.ItemNumber = b.product_ItemNumber
ORDER BY b.purchase_count DESC
