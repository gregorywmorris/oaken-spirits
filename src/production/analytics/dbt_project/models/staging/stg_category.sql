select
    CategoryNumber,
    CategoryName
from {{ source('oaken', 'category') }}