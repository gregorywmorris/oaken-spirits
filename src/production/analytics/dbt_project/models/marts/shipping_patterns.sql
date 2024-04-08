WITH vendor AS (
  SELECT 
    VendorNumber,
    VendorName
  FROM {{ ref('stg_vendor') }}
),
product AS (
  SELECT 
    ItemNumber,
    ItemDescription
  FROM {{ ref('stg_product') }}
),
customer AS (
  SELECT
    StoreNumber,
    StoreName
  FROM {{ ref('stg_customer') }}
)

SELECT 
  c.StoreName,
  v.VendorName,
  p.ItemDescription,
  s.SaleDate,
  s.ShippingDate,
  DATE_DIFF(TIMESTAMP(s.ShippingDate), TIMESTAMP(s.SaleDate), DAY) AS DaysToDeliver
FROM {{ ref('stg_sales') }} s
LEFT JOIN vendor v ON s.VendorNumber = v.VendorNumber
LEFT JOIN product p ON s.ItemNumber = p.ItemNumber
LEFT JOIN customer c ON s.StoreNumber = c.StoreNumber
ORDER BY DaysToDeliver DESC
