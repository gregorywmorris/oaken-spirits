select
    title_id,
    title
from {{ source('oaken', 'positions') }}