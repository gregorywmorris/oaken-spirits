select
    Invoice,
    StoreNumber
    VendorNumber,
    SalesDate,
    SalesDollars,
    ItemNumber,
    VolumeSoldLiters,
    ShippingDate,
    ShippingCost
from {{ source('oaken', 'sales') }}
