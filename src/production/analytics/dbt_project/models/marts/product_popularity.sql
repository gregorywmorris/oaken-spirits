WITH base AS (
  SELECT 
    item_id,
    COUNT(item_id) AS purchase_count
  FROM {{ ref('stg_sales') }}
  GROUP BY item_id
)

SELECT 
  product.item_id,
  product.item_description,
  base.purchase_count
FROM {{ ref('stg_products') }} product
LEFT JOIN base ON product.item_id = base.item_id
ORDER BY base.purchase_count DESC
