SELECT
    s.Invoice,
    s.SaleDate,
    s.SaleDollars,
    s.BottlesSold,
    s.VolumeSoldLiters,
    s.ShippingDate,
    s.ShippingCost,
    p.ItemDescription,
    c.CategoryName,
    cus.StoreName,
    v.VendorName
FROM {{ ref('stg_sales') }} s
LEFT JOIN {{ ref('stg_product') }} p ON s.ItemNumber = p.ItemNumber
LEFT JOIN {{ ref('stg_category') }} c ON p.CategoryNumber = c.CategoryNumber
LEFT JOIN {{ ref('stg_customer') }} cus ON s.StoreNumber = cus.StoreNumber
LEFT JOIN {{ ref('stg_vendor') }} v ON s.VendorNumber = v.VendorNumber
ORDER BY s.SaleDate ASC