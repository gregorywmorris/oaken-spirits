WITH base AS (
  SELECT
    p.item_id,
    p.item_description,
    SUM(s.sale_amount_dollar) AS total_sales_dollar
  FROM {{ ref('stg_sales') }} s
  JOIN {{ ref('stg_products') }} p ON s.item_id = p.item_id
  GROUP BY p.item_id, p.item_description
  ORDER BY total_sales_dollar DESC
  LIMIT 10
)
SELECT
    p.item_description,
    s.sale_date,
    SUM(s.sale_amount_dollar) AS total_sales_dollar,
    SUM(s.bottle_count) AS total_bottles_sold
FROM {{ ref('stg_sales') }} s
JOIN base b ON s.item_id = b.item_id
LEFT JOIN {{ ref('stg_products') }}  p ON s.item_id = p.item_id
GROUP BY p.item_description, s.sale_date
ORDER BY s.sale_date ASC