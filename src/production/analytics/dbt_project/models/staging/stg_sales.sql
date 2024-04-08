select
    Invoice,
    StoreNumber,
    VendorNumber,
    SaleDate,
    SaleDollars,
    ItemNumber,
    VolumeSoldLiters,
    ShippingDate,
    ShippingCost
from {{ source('oaken', 'sales') }}
