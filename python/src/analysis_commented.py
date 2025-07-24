"""
City Liability Analysis - Statistical Analysis Module

This module performs comprehensive statistical analysis and visualization of liability claims data.
Generates interactive charts, trend analysis, and business intelligence reports for municipal
risk management and strategic decision-making.

Author: Data Analysis Team
Date: July 2025
Project: City Liability Analytics
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import sqlite3
import os

def perform_analysis(db_path):
    """
    Perform comprehensive statistical analysis of liability claims data.
    
    This function conducts multi-faceted analysis including:
    - Temporal trend analysis (monthly, quarterly patterns)
    - Incident type cost analysis and ranking
    - City division performance evaluation
    - Claim status distribution analysis
    - Interactive visualization generation
    
    Args:
        db_path (str): Path to the SQLite database containing claims data
    
    Returns:
        None: Generates visualization files and provides console output
    """
    
    # Setup output directory for generated visualizations
    print("🚀 Starting City Liability Statistical Analysis")
    print("=" * 60)
    
    output_dir = os.path.join('..', '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory: {os.path.abspath(output_dir)}")

    # Database connection and data extraction
    print(f"🔗 Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    
    try:
        # Verify database structure
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📋 Tables found: {tables}")
        
        # Extract all claims data for comprehensive analysis
        print("📊 Loading claims data for analysis...")
        df = pd.read_sql("SELECT * FROM claims", conn)
        print(f"✅ Successfully loaded {len(df)} rows from claims table")
        
    except Exception as e:
        print(f"❌ Error reading data from database: {e}")
        conn.close()
        return
    finally:
        # Always close database connection
        conn.close()

    # Data preprocessing and feature engineering
    print("🔄 Preprocessing data for analysis...")
    
    # Convert date columns to datetime objects for temporal analysis
    date_columns = ['Date_of_Incident', 'Date_Claim_Filed']
    for date_col in date_columns:
        print(f"📅 Converting {date_col} to datetime...")
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

    # Remove records with invalid incident dates (data quality control)
    initial_count = len(df)
    df.dropna(subset=['Date_of_Incident'], inplace=True)
    removed_count = initial_count - len(df)
    if removed_count > 0:
        print(f"🧹 Removed {removed_count} records with invalid dates")

    # Feature engineering for temporal analysis
    print("⚙️ Creating temporal features...")
    df['Year'] = df['Date_of_Incident'].dt.year
    df['Month'] = df['Date_of_Incident'].dt.month
    df['Quarter'] = df['Date_of_Incident'].dt.to_period('Q').astype(str)  # Convert to string for plotting
    
    # Calculate total financial impact per claim
    df['Total_Loss'] = df['Settlement_Amount'] + df['Legal_Costs']
    print(f"💰 Total financial exposure: ${df['Total_Loss'].sum():,.2f}")

    # --- LOSS FREQUENCY & SEVERITY ANALYSIS ---
    print("\n📈 Performing Loss Frequency & Severity Analysis...")

    # 1. MONTHLY CLAIM FREQUENCY ANALYSIS
    print("📊 Analyzing monthly claim frequency trends...")
    
    # Group claims by month and count frequency
    claims_by_month = df.groupby(
        pd.Grouper(key='Date_of_Incident', freq='ME')  # Month-end frequency
    ).size().reset_index(name='Claim_Count')
    
    # Format dates for better visualization
    claims_by_month['Date_of_Incident'] = claims_by_month['Date_of_Incident'].dt.strftime('%Y-%m')
    
    # Create interactive time series chart
    fig_time = px.line(
        claims_by_month, 
        x='Date_of_Incident', 
        y='Claim_Count',
        title='Monthly Claim Frequency Over Time - Trend Analysis',
        labels={
            'Date_of_Incident': 'Month', 
            'Claim_Count': 'Number of Claims'
        },
        template='plotly_white'
    )
    
    # Enhance chart readability
    fig_time.update_xaxes(tickangle=45)
    fig_time.update_layout(
        hovermode='x unified',
        showlegend=False
    )
    
    # Save interactive chart
    output_file = os.path.join(output_dir, "monthly_claim_frequency.html")
    fig_time.write_html(output_file)
    print(f"✅ Saved: {output_file}")

    # 2. TOP INCIDENT TYPES BY TOTAL LOSS ANALYSIS
    print("🔍 Analyzing incident types by financial impact...")
    
    # Calculate total loss by incident type and rank top 10
    top_incident_types_loss = (
        df.groupby('Incident_Type')['Total_Loss']
        .sum()
        .nlargest(10)
        .reset_index()
    )
    
    # Create interactive bar chart with color coding
    fig_inc_type_loss = px.bar(
        top_incident_types_loss, 
        x='Incident_Type', 
        y='Total_Loss',
        title='Top 10 Incident Types by Total Financial Loss',
        labels={
            'Incident_Type': 'Incident Type', 
            'Total_Loss': 'Total Loss Amount ($)'
        },
        color='Total_Loss', 
        color_continuous_scale=px.colors.sequential.Plasma,
        template='plotly_white'
    )
    
    # Format for better readability
    fig_inc_type_loss.update_layout(
        xaxis_title="Incident Type", 
        yaxis_title="Total Loss Amount ($)",
        xaxis_tickangle=45
    )
    
    # Save visualization
    output_file = os.path.join(output_dir, "top_incident_types_loss.html")
    fig_inc_type_loss.write_html(output_file)
    print(f"✅ Saved: {output_file}")

    # 3. TOP CITY DIVISIONS BY TOTAL LOSS ANALYSIS
    print("🏛️ Analyzing city divisions by financial impact...")
    
    # Calculate total loss by city division and rank top 10
    top_divisions_loss = (
        df.groupby('City_Division_Involved')['Total_Loss']
        .sum()
        .nlargest(10)
        .reset_index()
    )
    
    # Create interactive visualization
    fig_div_loss = px.bar(
        top_divisions_loss, 
        x='City_Division_Involved', 
        y='Total_Loss',
        title='Top 10 City Divisions by Total Financial Loss',
        labels={
            'City_Division_Involved': 'City Division', 
            'Total_Loss': 'Total Loss Amount ($)'
        },
        color='Total_Loss', 
        color_continuous_scale=px.colors.sequential.Viridis,
        template='plotly_white'
    )
    
    # Enhance readability
    fig_div_loss.update_layout(
        xaxis_title="City Division", 
        yaxis_title="Total Loss Amount ($)",
        xaxis_tickangle=45
    )
    
    # Save visualization
    output_file = os.path.join(output_dir, "top_divisions_loss.html")
    fig_div_loss.write_html(output_file)
    print(f"✅ Saved: {output_file}")

    # 4. CLAIMS STATUS DISTRIBUTION ANALYSIS
    print("📋 Analyzing claim status distribution...")
    
    # Calculate percentage distribution of claim statuses
    claim_status_dist = (
        df['Claim_Status']
        .value_counts(normalize=True)
        .reset_index()
    )
    claim_status_dist.columns = ['Claim_Status', 'Percentage']
    
    # Create interactive pie chart
    fig_status = px.pie(
        claim_status_dist, 
        values='Percentage', 
        names='Claim_Status',
        title='Distribution of Claim Resolution Status',
        template='plotly_white'
    )
    
    # Enhance pie chart formatting
    fig_status.update_traces(
        textposition='inside', 
        textinfo='percent+label'
    )
    
    # Save visualization
    output_file = os.path.join(output_dir, "claim_status_distribution.html")
    fig_status.write_html(output_file)
    print(f"✅ Saved: {output_file}")

    # 5. QUARTERLY COST ANALYSIS BY DIVISION (Static Visualization)
    print("📊 Creating quarterly cost analysis by division...")
    
    # Calculate quarterly average cost per claim by division
    quarterly_avg_cost = (
        df.groupby(['Quarter', 'City_Division_Involved'])['Total_Loss']
        .mean()
        .reset_index()
    )
    
    # Filter for top 5 divisions with most data points for clearer visualization
    significant_divisions = df['City_Division_Involved'].value_counts().nlargest(5).index
    quarterly_avg_cost_filtered = quarterly_avg_cost[
        quarterly_avg_cost['City_Division_Involved'].isin(significant_divisions)
    ]

    # Create professional static visualization using matplotlib/seaborn
    plt.figure(figsize=(14, 8))
    sns.lineplot(
        data=quarterly_avg_cost_filtered, 
        x='Quarter', 
        y='Total_Loss', 
        hue='City_Division_Involved', 
        marker='o',
        linewidth=2,
        markersize=6
    )
    
    # Enhance chart appearance
    plt.title('Quarterly Average Loss Per Claim by Top City Divisions', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Quarter', fontsize=12, fontweight='bold')
    plt.ylabel('Average Loss ($)', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='City Division', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # Save static chart
    output_file = os.path.join(output_dir, "quarterly_avg_cost_per_claim_division.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()  # Close plot to free memory
    print(f"✅ Saved: {output_file}")

    # ANALYSIS SUMMARY
    print("\n📊 ANALYSIS SUMMARY")
    print("=" * 40)
    print(f"📈 Total Claims Analyzed: {len(df):,}")
    print(f"📅 Date Range: {df['Date_of_Incident'].min().strftime('%Y-%m-%d')} to {df['Date_of_Incident'].max().strftime('%Y-%m-%d')}")
    print(f"💰 Total Financial Exposure: ${df['Total_Loss'].sum():,.2f}")
    print(f"📊 Average Cost per Claim: ${df['Total_Loss'].mean():.2f}")
    print(f"🏛️ City Divisions Analyzed: {df['City_Division_Involved'].nunique()}")
    print(f"🔍 Incident Types: {df['Incident_Type'].nunique()}")
    
    print(f"\n📁 Generated Visualizations:")
    print(f"   • Monthly claim frequency trends")
    print(f"   • Top incident types by financial impact")
    print(f"   • City division performance analysis")
    print(f"   • Claim status distribution")
    print(f"   • Quarterly cost trends by division")
    
    print(f"\n✅ Loss Frequency & Severity Analysis complete!")
    print(f"📂 Check '{output_dir}' directory for all generated visualizations.")

if __name__ == "__main__":
    """
    Main execution block for statistical analysis.
    
    Defines database path and initiates comprehensive analysis workflow.
    """
    
    # Define database path relative to project structure
    db_file_path = os.path.join('..', '..', 'data', 'processed', 'city_claims.db')
    
    # Execute comprehensive analysis
    perform_analysis(db_file_path)
