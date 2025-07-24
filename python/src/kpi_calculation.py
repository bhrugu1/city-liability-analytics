import pandas as pd
import sqlite3
import os

def calculate_kpis(db_path):
    # Ensure the processed data directory exists
    processed_dir = os.path.join('..', '..', 'data', 'processed')
    os.makedirs(processed_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM claims", conn)
    except Exception as e:
        print(f"Error reading data from database: {e}")
        conn.close()
        return
    finally:
        conn.close()

    df['Date_of_Incident'] = pd.to_datetime(df['Date_of_Incident'], errors='coerce')
    df['Date_Claim_Filed'] = pd.to_datetime(df['Date_Claim_Filed'], errors='coerce')

    # Drop rows where Date_of_Incident is NaT after conversion
    df.dropna(subset=['Date_of_Incident'], inplace=True)

    df['Total_Loss'] = df['Settlement_Amount'] + df['Legal_Costs']
    df['Quarter'] = df['Date_of_Incident'].dt.to_period('Q') # Group by quarter

    kpis_data = []
    for quarter, group in df.groupby('Quarter'):
        total_claims = len(group)
        total_loss = group['Total_Loss'].sum()
        avg_cost_per_claim = total_loss / total_claims if total_claims > 0 else 0

        # Calculate Claim Resolution Rate: percentage of claims closed within the quarter
        # This is a simplified approach; a more robust one would track claim lifecycle.
        resolved_claims = group[group['Claim_Status'].isin(['Closed - Settled', 'Closed - Denied', 'Closed - Withdrawn'])]
        claim_resolution_rate = len(resolved_claims) / total_claims if total_claims > 0 else 0

        # Example of another KPI: Average Days to Close Claim (for closed claims)
        closed_claims = group[group['Claim_Status'].str.startswith('Closed')].copy()
        if not closed_claims.empty:
            closed_claims['Days_to_Close'] = (closed_claims['Date_Claim_Filed'] - closed_claims['Date_of_Incident']).dt.days
            avg_days_to_close = closed_claims['Days_to_Close'].mean()
        else:
            avg_days_to_close = 0


        kpis_data.append({
            'Quarter': str(quarter), # Convert Period object to string for CSV
            'Total_Claims': total_claims,
            'Total_Loss': total_loss,
            'Avg_Cost_per_Claim': avg_cost_per_claim,
            'Claim_Resolution_Rate': claim_resolution_rate,
            'Avg_Days_to_Close_Claim': avg_days_to_close
        })

    df_kpis = pd.DataFrame(kpis_data)
    kpis_csv_path = os.path.join(processed_dir, 'quarterly_kpis.csv')
    df_kpis.to_csv(kpis_csv_path, index=False)
    print(f"Quarterly KPIs calculated and saved to {kpis_csv_path}")
    return df_kpis

if __name__ == "__main__":
    db_file_path = os.path.join('..', '..', 'data', 'processed', 'city_claims.db')
    calculate_kpis(db_file_path)
