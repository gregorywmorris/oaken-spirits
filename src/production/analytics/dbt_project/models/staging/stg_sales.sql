select
    invoice,
    store_id,
    vendor_id,
    employee_id,
    sale_date,
    sale_amount_dollar,
    item_id,
    bottle_count,
    volume_liter,
    shipping_date,
    shipping_cost
from {{ source('oaken_bigquery', 'sales') }}
