SELECT 
  customers.Store_name,
  vendors.vendor_name
  products.item_description,
  sales.sale_date,
  sales.shipping_date,
  DATE_DIFF(TIMESTAMP(sales.shipping_date), TIMESTAMP(sales.sale_date), DAY) AS days_to_deliver
FROM {{ ref('stg_sales') }} sales
LEFT JOIN {{ ref('stg_vendors') }} vendors ON sales.vendor_id = vendors.vendor_id
LEFT JOIN {{ ref('stg_products') }} products ON sales.item_id = products.item_id
LEFT JOIN {{ ref('stg_customers') }} customers ON sales.store_id = customers.store_id
ORDER BY DaysToDeliver DESC
