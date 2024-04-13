CREATE OR REPLACE MODEL `oaken_transformed.category_forecast`

OPTIONS(
  MODEL_TYPE='ARIMA',
  TIME_SERIES_TIMESTAMP_COL='SaleDate', 
  TIME_SERIES_DATA_COL='TotalSalesDollars',
  TIME_SERIES_ID_COL='CategoryName',
  HOLIDAY_REGION='US'
) AS

SELECT  SaleDate, CategoryName, TotalSalesDollars
FROM `your project name.oaken_transformed.top_ten_forecast`