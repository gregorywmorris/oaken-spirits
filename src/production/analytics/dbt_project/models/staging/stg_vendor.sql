select
    VendorNumber,
    VendorName
from {{ source('oaken', 'vendors') }}