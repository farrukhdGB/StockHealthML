# Import necessary libraries
from imports import *

# Function to fetch financial statements using yfinance
def get_financials(ticker):

    try:
        stock = yf.Ticker(ticker)
        income_stmt = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow
        return {'income': income_stmt, 'balance': balance_sheet, 'cash_flow': cash_flow}
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Function to extract financial metrics
def extract_metrics(financial_data):

    records = []
    for ticker, data in financial_data.items():
        if data is None:
            continue  # Skip if data fetching failed

        try:
            income = data['income']
            balance = data['balance']
            cash = data['cash_flow']

            revenue = income.loc['Total Revenue'].iloc[0] if 'Total Revenue' in income.index else np.nan
            net_income = income.loc['Net Income'].iloc[0] if 'Net Income' in income.index else np.nan
            operating_income = income.loc['Operating Income'].iloc[0] if 'Operating Income' in income.index else np.nan
            gross_profit = income.loc['Gross Profit'].iloc[0] if 'Gross Profit' in income.index else np.nan
            interest_expense = income.loc['Interest Expense'].iloc[0] if 'Interest Expense' in income.index else np.nan

            current_assets = balance.loc['Total Current Assets'].iloc[0] if 'Total Current Assets' in balance.index else np.nan
            current_liabilities = balance.loc['Total Current Liabilities'].iloc[0] if 'Total Current Liabilities' in balance.index else np.nan
            total_debt = balance.loc['Total Debt'].iloc[0] if 'Total Debt' in balance.index else np.nan
            total_equity = balance.loc['Total Stockholder Equity'].iloc[0] if 'Total Stockholder Equity' in balance.index else np.nan
            total_assets = balance.loc['Total Assets'].iloc[0] if 'Total Assets' in balance.index else np.nan

            operating_cash_flow = cash.loc['Total Cash From Operating Activities'].iloc[0] if 'Total Cash From Operating Activities' in cash.index else np.nan
            capital_expenditures = cash.loc['Capital Expenditures'].iloc[0] if 'Capital Expenditures' in cash.index else 0 

            # Calculate Ratios with error handling
            gross_margin = (gross_profit / revenue) * 100 if revenue and not np.isnan(gross_profit) else np.nan
            operating_margin = (operating_income / revenue) * 100 if revenue and not np.isnan(operating_income) else np.nan
            net_margin = (net_income / revenue) * 100 if revenue and not np.isnan(net_income) else np.nan
            current_ratio = current_assets / current_liabilities if current_liabilities and not np.isnan(current_assets) else np.nan
            debt_to_equity = total_debt / total_equity if total_equity and not np.isnan(total_debt) else np.nan
            interest_coverage = operating_income / interest_expense if interest_expense and not np.isnan(operating_income) else np.nan
            asset_turnover = revenue / total_assets if total_assets and not np.isnan(revenue) else np.nan
            free_cash_flow = operating_cash_flow - capital_expenditures if not np.isnan(operating_cash_flow) else np.nan

            # Append the record
            record = {
                'Ticker': ticker,
                'Revenue': revenue,
                'Net Income': net_income,
                'Operating Income': operating_income,
                'Gross Margin': gross_margin,
                'Operating Margin': operating_margin,
                'Net Margin': net_margin,
                'Current Ratio': current_ratio,
                'Debt to Equity': debt_to_equity,
                'Interest Coverage': interest_coverage,
                'Asset Turnover': asset_turnover,
                'Free Cash Flow': free_cash_flow
            }
            records.append(record)
        except Exception as e:
            print(f"Error processing data for {ticker}: {e}")

    df = pd.DataFrame(records)
    return df


def predict_financial_health(ticker, scaler, model_rf, financial_data, financial_df, features):

    numeric_cols = financial_df.select_dtypes(include=[np.number]).columns

    data = get_financials(ticker)
    if data is None:
        print(f"Failed to fetch data for {ticker}.")
        return

    try:
        income = data['income']
        balance = data['balance']
        cash = data['cash_flow']

        revenue = income.loc['Total Revenue'].iloc[0] if 'Total Revenue' in income.index else np.nan
        net_income = income.loc['Net Income'].iloc[0] if 'Net Income' in income.index else np.nan
        operating_income = income.loc['Operating Income'].iloc[0] if 'Operating Income' in income.index else np.nan
        gross_profit = income.loc['Gross Profit'].iloc[0] if 'Gross Profit' in income.index else np.nan
        interest_expense = income.loc['Interest Expense'].iloc[0] if 'Interest Expense' in income.index else np.nan

        current_assets = balance.loc['Total Current Assets'].iloc[0] if 'Total Current Assets' in balance.index else np.nan
        current_liabilities = balance.loc['Total Current Liabilities'].iloc[0] if 'Total Current Liabilities' in balance.index else np.nan
        total_debt = balance.loc['Total Debt'].iloc[0] if 'Total Debt' in balance.index else np.nan
        total_equity = balance.loc['Total Stockholder Equity'].iloc[0] if 'Total Stockholder Equity' in balance.index else np.nan
        total_assets = balance.loc['Total Assets'].iloc[0] if 'Total Assets' in balance.index else np.nan

        operating_cash_flow = cash.loc['Total Cash From Operating Activities'].iloc[0] if 'Total Cash From Operating Activities' in cash.index else np.nan
        capital_expenditures = cash.loc['Capital Expenditures'].iloc[0] if 'Capital Expenditures' in cash.index else 0

        gross_margin = (gross_profit / revenue) * 100 if revenue and not np.isnan(gross_profit) else np.nan
        operating_margin = (operating_income / revenue) * 100 if revenue and not np.isnan(operating_income) else np.nan
        net_margin = (net_income / revenue) * 100 if revenue and not np.isnan(net_income) else np.nan
        current_ratio = current_assets / current_liabilities if current_liabilities and not np.isnan(current_assets) else np.nan
        debt_to_equity = total_debt / total_equity if total_equity and not np.isnan(total_debt) else np.nan
        interest_coverage = operating_income / interest_expense if interest_expense and not np.isnan(operating_income) else np.nan
        asset_turnover = revenue / total_assets if total_assets and not np.isnan(revenue) else np.nan
        free_cash_flow = operating_cash_flow - capital_expenditures if not np.isnan(operating_cash_flow) else np.nan

        # Create a DataFrame for the specific ticker
        xyz_record = {
            'Revenue': revenue,
            'Net Income': net_income,
            'Operating Income': operating_income,
            'Gross Margin': gross_margin,
            'Operating Margin': operating_margin,
            'Net Margin': net_margin,
            'Current Ratio': current_ratio,
            'Debt to Equity': debt_to_equity,
            'Interest Coverage': interest_coverage,
            'Asset Turnover': asset_turnover,
            'Free Cash Flow': free_cash_flow
        }
        xyz_df = pd.DataFrame([xyz_record])

        xyz_df[numeric_cols] = xyz_df[numeric_cols].fillna(financial_df[numeric_cols].mean())

        xyz_scaled = scaler.transform(xyz_df)
        xyz_scaled_df = pd.DataFrame(xyz_scaled, columns=features.columns)

        xyz_health_rf = model_rf.predict(xyz_scaled_df)[0]
        xyz_prob_rf = model_rf.predict_proba(xyz_scaled_df)[0][xyz_health_rf]

        health_rf = 'Healthy' if xyz_health_rf == 1 else 'Unhealthy'

        print(f"\nRandom Forest Prediction for {ticker}: {health_rf} (Probability: {xyz_prob_rf:.2f})")

    except Exception as e:
        print(f"Error processing data for {ticker}: {e}")
