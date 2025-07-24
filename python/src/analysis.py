import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import sqlite3
import os

def perform_analysis(db_path):
    # Ensure the output directory exists for saving plots
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    print(f"Connected to database: {db_path}")
    
    # Check if file exists and tables
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables found: {tables}")
        
        df = pd.read_sql("SELECT * FROM claims", conn)
        print(f"Successfully loaded {len(df)} rows from claims table")
    except Exception as e:
        print(f"Error reading data from database: {e}")
        conn.close()
        return
    finally:
        conn.close()

    # Convert date columns to datetime objects
    df['Date_of_Incident'] = pd.to_datetime(df['Date_of_Incident'], errors='coerce')
    df['Date_Claim_Filed'] = pd.to_datetime(df['Date_Claim_Filed'], errors='coerce')

    # Drop rows where Date_of_Incident is NaT after conversion
    df.dropna(subset=['Date_of_Incident'], inplace=True)

    df['Year'] = df['Date_of_Incident'].dt.year
    df['Month'] = df['Date_of_Incident'].dt.month
    df['Quarter'] = df['Date_of_Incident'].dt.to_period('Q').astype(str) # Convert to string for plotting consistency
    df['Total_Loss'] = df['Settlement_Amount'] + df['Legal_Costs']

    # --- Loss Frequency & Severity Analysis ---

    print("Performing Loss Frequency & Severity Analysis...")

    # 1. Monthly Claim Frequency
    claims_by_month = df.groupby(pd.Grouper(key='Date_of_Incident', freq='M')).size().reset_index(name='Claim_Count')
    claims_by_month['Date_of_Incident'] = claims_by_month['Date_of_Incident'].dt.strftime('%Y-%m') # Format for better x-axis labels
    fig_time = px.line(claims_by_month, x='Date_of_Incident', y='Claim_Count',
                       title='Monthly Claim Frequency Over Time',
                       labels={'Date_of_Incident': 'Month', 'Claim_Count': 'Number of Claims'},
                       template='plotly_white')
    fig_time.update_xaxes(tickangle=45)
    fig_time.write_html(os.path.join(output_dir, "monthly_claim_frequency.html"))
    print(f"Saved: {os.path.join(output_dir, 'monthly_claim_frequency.html')}")

    # 2. Top 10 Incident Types by Total Loss
    top_incident_types_loss = df.groupby('Incident_Type')['Total_Loss'].sum().nlargest(10).reset_index()
    fig_inc_type_loss = px.bar(top_incident_types_loss, x='Incident_Type', y='Total_Loss',
                               title='Top 10 Incident Types by Total Loss',
                               labels={'Incident_Type': 'Incident Type', 'Total_Loss': 'Total Loss Amount ($)'},
                               color='Total_Loss', color_continuous_scale=px.colors.sequential.Plasma,
                               template='plotly_white')
    fig_inc_type_loss.update_layout(xaxis_title="Incident Type", yaxis_title="Total Loss Amount ($)")
    fig_inc_type_loss.write_html(os.path.join(output_dir, "top_incident_types_loss.html"))
    print(f"Saved: {os.path.join(output_dir, 'top_incident_types_loss.html')}")

    # 3. Top 10 City Divisions by Total Loss
    top_divisions_loss = df.groupby('City_Division_Involved')['Total_Loss'].sum().nlargest(10).reset_index()
    fig_div_loss = px.bar(top_divisions_loss, x='City_Division_Involved', y='Total_Loss',
                          title='Top 10 City Divisions by Total Loss',
                          labels={'City_Division_Involved': 'City Division', 'Total_Loss': 'Total Loss Amount ($)'},
                          color='Total_Loss', color_continuous_scale=px.colors.sequential.Viridis,
                          template='plotly_white')
    fig_div_loss.update_layout(xaxis_title="City Division", yaxis_title="Total Loss Amount ($)")
    fig_div_loss.write_html(os.path.join(output_dir, "top_divisions_loss.html"))
    print(f"Saved: {os.path.join(output_dir, 'top_divisions_loss.html')}")

    # 4. Claims Status Distribution
    claim_status_dist = df['Claim_Status'].value_counts(normalize=True).reset_index()
    claim_status_dist.columns = ['Claim_Status', 'Percentage']
    fig_status = px.pie(claim_status_dist, values='Percentage', names='Claim_Status',
                        title='Distribution of Claim Statuses',
                        template='plotly_white')
    fig_status.write_html(os.path.join(output_dir, "claim_status_distribution.html"))
    print(f"Saved: {os.path.join(output_dir, 'claim_status_distribution.html')}")

    # 5. Quarterly Average Cost Per Claim by Division (Example using Matplotlib/Seaborn)
    # This shows how to use Matplotlib/Seaborn if you prefer static plots or more customization
    quarterly_avg_cost = df.groupby(['Quarter', 'City_Division_Involved'])['Total_Loss'].mean().reset_index()
    # Filter for divisions with significant data points for clearer visualization
    significant_divisions = df['City_Division_Involved'].value_counts().nlargest(5).index
    quarterly_avg_cost_filtered = quarterly_avg_cost[quarterly_avg_cost['City_Division_Involved'].isin(significant_divisions)]

    plt.figure(figsize=(14, 8))
    sns.lineplot(data=quarterly_avg_cost_filtered, x='Quarter', y='Total_Loss', hue='City_Division_Involved', marker='o')
    plt.title('Quarterly Average Loss Per Claim by Top Divisions')
    plt.xlabel('Quarter')
    plt.ylabel('Average Loss ($)')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "quarterly_avg_cost_per_claim_division.png"))
    plt.close() # Close plot to free memory
    print(f"Saved: {os.path.join(output_dir, 'quarterly_avg_cost_per_claim_division.png')}")

    print("\nLoss Frequency & Severity Analysis complete. Check 'output/' directory for generated visualizations.")

if __name__ == "__main__":
    # Path to your SQLite database
    db_file_path = os.path.join('..', '..', 'data', 'processed', 'city_claims.db')
    print(f"Database path: {os.path.abspath(db_file_path)}")
    perform_analysis(db_file_path)
