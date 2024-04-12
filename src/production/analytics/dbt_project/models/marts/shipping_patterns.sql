SELECT 
  c.StoreName,
  v.VendorName,
  p.ItemDescription,
  s.SaleDate,
  s.ShippingDate,
  DATE_DIFF(TIMESTAMP(s.ShippingDate), TIMESTAMP(s.SaleDate), DAY) AS DaysToDeliver
FROM {{ ref('stg_sales') }} s
LEFT JOIN {{ ref('stg_vendor') }} v ON s.VendorNumber = v.VendorNumber
LEFT JOIN {{ ref('stg_product') }} p ON s.ItemNumber = p.ItemNumber
LEFT JOIN {{ ref('stg_customer') }} c ON s.StoreNumber = c.StoreNumber
ORDER BY DaysToDeliver DESC
