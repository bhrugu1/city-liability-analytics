import pandas as pd

# Read the generated KPI file
df = pd.read_csv('../../data/processed/quarterly_kpis.csv')

print('KPI Summary:')
print('='*80)
print(df.head(10).to_string(index=False))
print(f'\nTotal quarters analyzed: {len(df)}')
print(f'Average claims per quarter: {df["Total_Claims"].mean():.0f}')
print(f'Average cost per claim overall: ${df["Avg_Cost_per_Claim"].mean():.2f}')
print(f'Average resolution rate: {df["Claim_Resolution_Rate"].mean():.2%}')
print(f'Average days to close: {df["Avg_Days_to_Close_Claim"].mean():.1f} days')
