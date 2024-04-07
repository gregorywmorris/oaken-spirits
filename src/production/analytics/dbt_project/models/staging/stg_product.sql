select
    ItemNumber,
    CategoryNumber,
    ItemDescription,
    BottleVolumeML,
    Pack,
    BottleCost,
    BottleRetail
from {{ source('oaken', 'product') }}
