WITH base AS (
  SELECT 
    item_id,
    COUNT(item_id) AS purchase_count
  FROM {{ ref('stg_sales') }}
  GROUP BY item_id
)

SELECT 
  p.item_id,
  p.item_description,
  b.purchase_count
FROM {{ ref('stg_products') }} p
LEFT JOIN base b ON p.item_id = b.item_id
ORDER BY b.purchase_count DESC
