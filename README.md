# StockHealthML
Check a company against top 50 companies to see if they are financially healthy or unhealthy before jumping in.

Install dependencies and run this block in jupyter notebook.

xyz_ticker = 'NOK' 

print(f"\nPredicting financial health for {xyz_ticker}...")

# Predict financial health for the specified ticker
fin.predict_financial_health(xyz_ticker, scaler, rf, financial_data, financial_df, features)
