select
    employee_id,
    first_name,
    last_name,
    title_id,
    manager,
    active
from {{ source('oaken_bigquery', 'employees') }}