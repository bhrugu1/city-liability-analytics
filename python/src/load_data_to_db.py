"""
City Liability Analysis - Database Loading Module

This module handles the ETL (Extract, Transform, Load) process for liability claims data.
It creates the database schema, processes CSV data, and loads it into SQLite for analysis.
Includes data validation, type conversion, and error handling for robust data pipeline.

Author: Data Analysis Team
Date: July 2025
Project: City Liability Analytics
"""

import pandas as pd
import sqlite3
import os

def load_csv_to_db(csv_path, db_path, table_name='claims'):
    """
    Load CSV data into SQLite database with proper schema and data validation.
    
    This function performs the complete ETL process:
    1. Creates database schema from SQL file
    2. Reads and validates CSV data
    3. Transforms data types for database compatibility
    4. Loads data with error handling and validation
    
    Args:
        csv_path (str): Path to the source CSV file
        db_path (str): Path to the target SQLite database
        table_name (str): Name of the database table (default: 'claims')
    
    Returns:
        None: Function provides console feedback on success/failure
    """
    
    # Ensure the processed data directory exists
    print("📁 Setting up database directory structure...")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Establish database connection
    print(f"🔗 Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the schema creation script for proper table structure
    try:
        print("🏗️ Creating/verifying database schema...")
        # Use path relative to project root for schema file
        schema_path = os.path.join('..', '..', 'sql', 'schema.sql')
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema creation with proper error handling
        cursor.executescript(schema_sql)
        print("✅ Database schema created/verified successfully.")
        
    except FileNotFoundError:
        print("❌ Error: sql/schema.sql not found. Please ensure the file exists.")
        conn.close()
        return
    except Exception as e:
        print(f"❌ Error creating schema: {e}")
        conn.close()
        return

    # Read and validate CSV data
    try:
        print(f"📖 Reading CSV data from: {csv_path}")
        df = pd.read_csv(csv_path)
        print(f"📊 Loaded {len(df)} records with {len(df.columns)} columns")
        
    except FileNotFoundError:
        print(f"❌ Error: CSV file not found at {csv_path}")
        print("💡 Please run data_simulation.py first to generate the data.")
        conn.close()
        return
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        conn.close()
        return

    # Data transformation and cleaning for database compatibility
    print("🔄 Transforming data for database compatibility...")
    
    # Convert date columns to appropriate format for SQL (YYYY-MM-DD)
    # Using errors='coerce' to handle any malformed dates gracefully
    date_columns = ['Date_of_Incident', 'Date_Claim_Filed']
    for date_col in date_columns:
        if date_col in df.columns:
            print(f"📅 Converting {date_col} to proper date format...")
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce').dt.strftime('%Y-%m-%d')

    # Handle potential NaN values in numeric columns before loading to SQL
    # This ensures data integrity and prevents SQLite errors
    numeric_cols = ['Settlement_Amount', 'Legal_Costs', 'Latitude', 'Longitude']
    for col in numeric_cols:
        if col in df.columns:
            print(f"🔢 Cleaning numeric data in {col}...")
            # Convert to numeric and fill NaNs with 0 (or appropriate default)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Data quality validation
    print("🔍 Performing data quality checks...")
    
    # Check for any remaining null values in critical columns
    critical_columns = ['Claim_ID', 'Date_of_Incident', 'Incident_Type']
    for col in critical_columns:
        if col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                print(f"⚠️ Warning: {null_count} null values found in {col}")

    # Load DataFrame to SQL table with comprehensive error handling
    try:
        print(f"💾 Loading data into '{table_name}' table...")
        
        # if_exists='replace' will overwrite existing data for clean reloads
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        # Verify successful loading
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        record_count = cursor.fetchone()[0]
        
        print(f"✅ Successfully loaded {record_count} records into '{table_name}' table")
        print(f"🎯 Database location: {db_path}")
        
        # Provide summary statistics
        total_settlement = df['Settlement_Amount'].sum() if 'Settlement_Amount' in df.columns else 0
        total_legal_costs = df['Legal_Costs'].sum() if 'Legal_Costs' in df.columns else 0
        print(f"💰 Total financial exposure loaded: ${total_settlement + total_legal_costs:,.2f}")
        
    except Exception as e:
        print(f"❌ Error loading data to SQL: {e}")
        print("💡 Check data format and database permissions")
    
    finally:
        # Always close database connection to prevent locks
        conn.close()
        print("🔒 Database connection closed")

if __name__ == "__main__":
    """
    Main execution block for database loading process.
    
    Defines file paths and initiates the ETL process with proper error handling.
    Uses relative paths to work correctly from the project structure.
    """
    
    print("🚀 Starting City Liability Analysis - Database Loading Process")
    print("=" * 60)
    
    # Define paths relative to the project root structure
    csv_file = os.path.join('..', '..', 'data', 'raw', 'simulated_claims.csv')
    db_file = os.path.join('..', '..', 'data', 'processed', 'city_claims.db')
    
    # Display configuration
    print(f"📂 Source CSV: {csv_file}")
    print(f"🗄️ Target DB: {db_file}")
    print("-" * 60)
    
    # Execute the ETL process
    load_csv_to_db(csv_file, db_file)
    
    print("=" * 60)
    print("🏁 Database loading process completed!")
