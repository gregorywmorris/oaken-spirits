WITH base AS (
  SELECT
    products.item_id,
    customers.category_name,
    SUM(sales.sale_amount_dollar) AS total_sales_dollar
  FROM {{ ref('stg_sales') }} sales
  JOIN {{ ref('stg_product') }} products ON sales.item_id = products.item_id
  JOIN {{ ref('stg_category') }} customers ON products.category_id = customers.category_id
  GROUP BY products.item_id, customers.category_name
  ORDER BY total_sales_dollar DESC
  LIMIT 10
)
SELECT
    base.category_name,
    sales.sale_date,
    SUM(sales.sale_amount_dollar) AS total_sales_dollar,
    SUM(sales.bottle_count) AS total_bottles_sold
FROM {{ ref('stg_sales') }} sales
JOIN base ON sales.item_id = base.item_id
LEFT JOIN {{ ref('stg_product') }}  products ON sales.item_id = products.item_id
LEFT JOIN {{ ref('stg_category') }}  customers ON products.category_id = customers.category_id
GROUP BY base.category_name, sales.sale_date
ORDER BY sales.sale_date ASC