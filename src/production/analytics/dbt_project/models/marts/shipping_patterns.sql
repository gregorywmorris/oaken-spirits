WITH vendor AS (
  SELECT 
    VendorNumber,
    VendorName
  FROM {{ ref('stg_name') }}
  GROUP BY 1
),
product AS (
  SELECT 
    ItemNumber,
    ItemDescription
  FROM {{ ref('stg_product') }}
  GROUP BY 1
),
customer AS (
  SELECT
    StoreNumber,
    StoreName
  FROM {{ ref('stg_customer') }}
  GROUP BY 1
)

SELECT 
  c.StoreName,
  v.VendorName,
  p.ItemDescription,
  s.SaleDate,
  s.ShippingDate,
  TIMESTAMP_DIFF(s.SaleDate, s.ShippingDate, DAY) AS DaysToDeliver
FROM {{ ref('stg_sales') }} s
LEFT JOIN vendor v ON s.VendorNumber = v.VendorNumber
LEFT JOIN product p on s.ItemNumber = p.ItemNumber
LEFT JOIN customer c on s.StoreNumber = c.StoreNumber
ORDER BY DaysToDeliver DESC
