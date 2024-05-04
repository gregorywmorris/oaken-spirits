select
    item_id,
    category_id,
    item_description,
    bottle_volume_ml,
    pack,
    bottle_cost,
    bottle_retail
from {{ source('oaken', 'products') }}
