"""
Chicago City Liability Analysis - Key Performance Indicators (KPI) Calculation Module

This module calculates critical business performance metrics for Chicago municipal 
liability management. It provides quarterly performance tracking, operational 
efficiency metrics, and strategic insights specifically for Chicago city risk 
management decision-making across all municipal divisions.

Municipal Focus: Chicago city operations and performance
Geographic Scope: Chicago metropolitan area

Author: Chicago Municipal Data Analysis Team
Date: July 2025
Project: Chicago City Liability Analytics Platform
"""

import pandas as pd
import sqlite3
import os

def calculate_kpis(db_path):
    """
    Calculate comprehensive Key Performance Indicators (KPIs) for liability management.
    
    This function computes quarterly business metrics including:
    - Claim volume trends (frequency analysis)
    - Financial exposure metrics (cost analysis)
    - Operational efficiency indicators (resolution rates)
    - Performance benchmarking (processing times)
    
    The KPIs support strategic decision-making for:
    - Resource allocation optimization
    - Risk mitigation strategy development
    - Performance monitoring and improvement
    - Budget planning and forecasting
    
    Args:
        db_path (str): Path to SQLite database containing claims data
        
    Returns:
        pandas.DataFrame: Quarterly KPI metrics for further analysis
    """
    
    print("📊 Starting KPI Calculation for Municipal Liability Management")
    print("=" * 65)
    
    # Setup processed data directory for KPI outputs
    processed_dir = os.path.join('..', '..', 'data', 'processed')
    os.makedirs(processed_dir, exist_ok=True)
    print(f"📁 Output directory: {os.path.abspath(processed_dir)}")

    # Database connection and data extraction
    print(f"🔗 Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    
    try:
        # Extract comprehensive claims dataset
        df = pd.read_sql("SELECT * FROM claims", conn)
        print(f"✅ Successfully loaded {len(df)} claims for KPI analysis")
        
    except Exception as e:
        print(f"❌ Error reading data from database: {e}")
        conn.close()
        return None
    finally:
        conn.close()

    # Data Preprocessing and Feature Engineering
    print("🔄 Preprocessing data for KPI calculations...")
    
    # Convert date columns to datetime objects for temporal analysis
    date_columns = ['Date_of_Incident', 'Date_Claim_Filed']
    for date_col in date_columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        print(f"📅 Converted {date_col} to datetime format")

    # Data quality control: remove records with invalid incident dates
    initial_count = len(df)
    df.dropna(subset=['Date_of_Incident'], inplace=True)
    removed_count = initial_count - len(df)
    if removed_count > 0:
        print(f"🧹 Removed {removed_count} records with invalid incident dates")

    # Financial metrics calculation
    df['Total_Loss'] = df['Settlement_Amount'] + df['Legal_Costs']
    print(f"💰 Total financial exposure: ${df['Total_Loss'].sum():,.2f}")
    
    # Temporal grouping for quarterly analysis
    df['Quarter'] = df['Date_of_Incident'].dt.to_period('Q')
    quarters_analyzed = df['Quarter'].nunique()
    print(f"📈 Analyzing {quarters_analyzed} quarters of data")

    # --- QUARTERLY KPI CALCULATION ---
    print("\n📊 Calculating Quarterly Performance Metrics...")
    
    kpis_data = []
    
    # Iterate through each quarter to calculate comprehensive KPIs
    for quarter, group in df.groupby('Quarter'):
        print(f"📈 Processing Quarter: {quarter}")
        
        # --- PRIMARY VOLUME METRICS ---
        total_claims = len(group)
        total_loss = group['Total_Loss'].sum()
        avg_cost_per_claim = total_loss / total_claims if total_claims > 0 else 0
        
        # --- OPERATIONAL EFFICIENCY METRICS ---
        
        # Claim Resolution Rate: Percentage of claims with final status
        # This measures operational effectiveness in claim closure
        resolved_statuses = ['Closed - Settled', 'Closed - Denied', 'Closed - Withdrawn']
        resolved_claims = group[group['Claim_Status'].isin(resolved_statuses)]
        claim_resolution_rate = len(resolved_claims) / total_claims if total_claims > 0 else 0
        
        # --- PROCESSING TIME ANALYSIS ---
        
        # Average Days to Close: Processing efficiency for resolved claims
        # Measures organizational responsiveness and workflow efficiency
        closed_claims = group[group['Claim_Status'].str.startswith('Closed')].copy()
        
        if not closed_claims.empty:
            # Calculate processing time from incident to claim filing
            closed_claims['Days_to_Close'] = (
                closed_claims['Date_Claim_Filed'] - closed_claims['Date_of_Incident']
            ).dt.days
            
            # Handle negative or unrealistic values
            valid_processing_times = closed_claims['Days_to_Close'][
                closed_claims['Days_to_Close'] >= 0
            ]
            avg_days_to_close = valid_processing_times.mean() if not valid_processing_times.empty else 0
        else:
            avg_days_to_close = 0

        # --- FINANCIAL PERFORMANCE INDICATORS ---
        
        # Settlement vs. Legal Cost Ratio
        total_settlements = group['Settlement_Amount'].sum()
        total_legal_costs = group['Legal_Costs'].sum()
        settlement_ratio = (
            total_settlements / total_loss if total_loss > 0 else 0
        )
        
        # --- RISK SEVERITY METRICS ---
        
        # High-value claim percentage (claims > $50,000)
        high_value_threshold = 50000
        high_value_claims = group[group['Total_Loss'] > high_value_threshold]
        high_value_claim_rate = len(high_value_claims) / total_claims if total_claims > 0 else 0
        
        # Aggregate quarterly KPI data
        quarterly_kpis = {
            'Quarter': str(quarter),  # Convert Period object to string for CSV export
            'Total_Claims': total_claims,
            'Total_Loss': round(total_loss, 2),
            'Avg_Cost_per_Claim': round(avg_cost_per_claim, 2),
            'Claim_Resolution_Rate': round(claim_resolution_rate, 4),
            'Avg_Days_to_Close_Claim': round(avg_days_to_close, 1),
            'Settlement_Ratio': round(settlement_ratio, 4),
            'High_Value_Claim_Rate': round(high_value_claim_rate, 4),
            'Total_Settlements': round(total_settlements, 2),
            'Total_Legal_Costs': round(total_legal_costs, 2)
        }
        
        kpis_data.append(quarterly_kpis)
        
        # Display quarterly summary
        print(f"   📋 Claims: {total_claims}")
        print(f"   💰 Total Loss: ${total_loss:,.2f}")
        print(f"   📊 Resolution Rate: {claim_resolution_rate:.1%}")

    # Create comprehensive KPI DataFrame
    df_kpis = pd.DataFrame(kpis_data)
    
    # Save KPI results to CSV for further analysis and reporting
    kpis_csv_path = os.path.join(processed_dir, 'quarterly_kpis.csv')
    df_kpis.to_csv(kpis_csv_path, index=False)
    
    print(f"\n✅ Quarterly KPIs calculated and saved to: {kpis_csv_path}")
    
    # --- KPI SUMMARY ANALYTICS ---
    print("\n📊 KPI SUMMARY ANALYTICS")
    print("=" * 40)
    
    if not df_kpis.empty:
        # Overall performance metrics
        total_quarters = len(df_kpis)
        avg_quarterly_claims = df_kpis['Total_Claims'].mean()
        avg_resolution_rate = df_kpis['Claim_Resolution_Rate'].mean()
        avg_cost_per_claim = df_kpis['Avg_Cost_per_Claim'].mean()
        
        print(f"📈 Quarters Analyzed: {total_quarters}")
        print(f"📊 Average Quarterly Claims: {avg_quarterly_claims:.0f}")
        print(f"🎯 Average Resolution Rate: {avg_resolution_rate:.1%}")
        print(f"💰 Average Cost per Claim: ${avg_cost_per_claim:,.2f}")
        print(f"⏱️ Average Processing Time: {df_kpis['Avg_Days_to_Close_Claim'].mean():.1f} days")
        
        # Performance trends
        if total_quarters > 1:
            latest_quarter = df_kpis.iloc[-1]
            previous_quarter = df_kpis.iloc[-2]
            
            print(f"\n📈 QUARTERLY TRENDS (Latest vs. Previous):")
            claim_trend = latest_quarter['Total_Claims'] - previous_quarter['Total_Claims']
            cost_trend = latest_quarter['Avg_Cost_per_Claim'] - previous_quarter['Avg_Cost_per_Claim']
            resolution_trend = latest_quarter['Claim_Resolution_Rate'] - previous_quarter['Claim_Resolution_Rate']
            
            print(f"   📊 Claim Volume: {claim_trend:+.0f}")
            print(f"   💰 Average Cost: ${cost_trend:+,.2f}")
            print(f"   🎯 Resolution Rate: {resolution_trend:+.1%}")
    
    print(f"\n🎯 KPI calculation complete!")
    print(f"📁 Results saved for business intelligence and reporting.")
    
    return df_kpis

if __name__ == "__main__":
    """
    Main execution block for KPI calculation and business intelligence.
    
    Executes comprehensive quarterly performance analysis including:
    - Volume and frequency metrics
    - Financial performance indicators
    - Operational efficiency measures
    - Risk severity assessments
    """
    
    # Define database path relative to project structure
    db_file_path = os.path.join('..', '..', 'data', 'processed', 'city_claims.db')
    
    # Execute comprehensive KPI calculation
    quarterly_kpis = calculate_kpis(db_file_path)
    
    # Display final results summary
    if quarterly_kpis is not None and not quarterly_kpis.empty:
        print(f"\n📊 Generated {len(quarterly_kpis)} quarters of KPI data")
        print("📈 Ready for dashboard integration and executive reporting")
