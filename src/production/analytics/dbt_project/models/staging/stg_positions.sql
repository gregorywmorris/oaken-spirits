select
    title_id,
    title
from {{ source('oaken_bigquery', 'positions') }}