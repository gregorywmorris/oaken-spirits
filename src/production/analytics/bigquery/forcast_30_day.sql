select *
from
  ML.FORECAST(
    MODEL `your project name.oaken_transformed.category_forecast`,
    STRUCT(30 AS horizon,
          0.90 AS confidence_level)
  )