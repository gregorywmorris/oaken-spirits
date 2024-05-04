SELECT 
  c.Store_name,
  v.vendor_name
  p.item_description,
  s.sale_date,
  s.shipping_date,
  DATE_DIFF(TIMESTAMP(s.shipping_date), TIMESTAMP(s.sale_date), DAY) AS days_to_deliver
FROM {{ ref('stg_sales') }} s
LEFT JOIN {{ ref('stg_vendors') }} v ON s.vendor_id = v.vendor_id
LEFT JOIN {{ ref('stg_products') }} p ON s.item_id = p.item_id
LEFT JOIN {{ ref('stg_customers') }} c ON s.store_id = c.store_id
ORDER BY DaysToDeliver DESC
