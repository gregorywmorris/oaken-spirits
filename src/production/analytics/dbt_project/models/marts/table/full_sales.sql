SELECT
    sales.invoice,
    sales.sale_date,
    sales.sale_amount_dollar,
    sales.bottle_count,
    sales.volume_liter,
    sales.shipping_date,
    sales.shipping_cost,
    products.item_description,
    categories.category_name,
    customers.store_name,
    vendors.vendor_name,
    CONCAT(employees.first_name, ',', employees.last_name) AS full_name
FROM {{ ref('stg_sales') }} sales
LEFT JOIN {{ ref('stg_products') }} products ON sales.ItemNumber = products.ItemNumber
LEFT JOIN {{ ref('stg_categories') }} categories ON products.CategoryNumber = categories.CategoryNumber
LEFT JOIN {{ ref('stg_customers') }} customers ON sales.StoreNumber = cusales.StoreNumber
LEFT JOIN {{ ref('stg_vendors') }} vendors ON sales.VendorNumber = vendors.VendorNumber
LEFT JOIN {{ ref('stg_employees') }} employees ON sales.employee_id = employees.employee_id
ORDER BY sales.sale_date ASC