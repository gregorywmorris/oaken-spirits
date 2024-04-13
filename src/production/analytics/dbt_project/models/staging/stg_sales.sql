select
    Invoice,
    StoreNumber,
    VendorNumber,
    SaleDate,
    SaleDollars,
    ItemNumber,
    BottlesSold,
    VolumeSoldLiters,
    ShippingDate,
    ShippingCost
from {{ source('oaken', 'sales') }}
