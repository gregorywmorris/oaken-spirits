CREATE OR REPLACE MODEL `oaken_transformed.sales_forecast`

OPTIONS(
  MODEL_TYPE='ARIMA',
  TIME_SERIES_TIMESTAMP_COL='SaleDate', 
  TIME_SERIES_DATA_COL='TotalSalesDollars',
  HOLIDAY_REGION='US'
) AS

SELECT  SaleDate, TotalSalesDollars
FROM `your project name.oaken_transformed.sales_forecast_historical`