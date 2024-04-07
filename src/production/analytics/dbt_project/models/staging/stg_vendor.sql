select
    VendorNumber,
    VendorName
from {{ source('oaken', 'vendor') }}