select
    invoice,
    store_id,
    vendor_id,
    employee_id,
    sale_date,
    sale_amount,
    item_id,
    bottle_count,
    volume_liter,
    shipping_date,
    shipping_cost
from {{ source('oaken', 'sales') }}
