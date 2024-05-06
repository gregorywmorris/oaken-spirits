select
    store_id,
    Store_name,
    street_address,
    city,
    county,
    us_state,
    zip_code
from {{ source('oaken_bigquery', 'customers') }}
