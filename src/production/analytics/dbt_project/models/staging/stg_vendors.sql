select
    vendor_id,
    vendor_name
from {{ source('oaken', 'vendors') }}