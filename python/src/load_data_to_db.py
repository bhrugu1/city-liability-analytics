import pandas as pd
import sqlite3
import os

def load_csv_to_db(csv_path, db_path, table_name='claims'):
    # Ensure the processed data directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the schema creation script
    try:
        # Use path relative to project root
        schema_path = os.path.join('..', '..', 'sql', 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        print("Database schema created/verified.")
    except FileNotFoundError:
        print("Error: sql/schema.sql not found. Please ensure the file exists.")
        conn.close()
        return
    except Exception as e:
        print(f"Error creating schema: {e}")
        conn.close()
        return

    # Read the CSV data
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}. Please run data_simulation.py first.")
        conn.close()
        return
    except Exception as e:
        print(f"Error reading CSV: {e}")
        conn.close()
        return

    # Convert date columns to appropriate format for SQL (YYYY-MM-DD)
    # Using errors='coerce' to turn unparseable dates into NaT (Not a Time)
    df['Date_of_Incident'] = pd.to_datetime(df['Date_of_Incident'], errors='coerce').dt.strftime('%Y-%m-%d')
    df['Date_Claim_Filed'] = pd.to_datetime(df['Date_Claim_Filed'], errors='coerce').dt.strftime('%Y-%m-%d')

    # Handle potential NaN values in numeric columns before loading to SQL
    numeric_cols = ['Settlement_Amount', 'Legal_Costs', 'Latitude', 'Longitude']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) # Fill NaNs with 0 or a suitable default

    # Load DataFrame to SQL table. if_exists='replace' will overwrite existing data.
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data from {csv_path} loaded successfully into '{table_name}' table in {db_path}")
    except Exception as e:
        print(f"Error loading data to SQL: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Define paths relative to the project root
    csv_file = os.path.join('..', '..', 'data', 'raw', 'simulated_claims.csv')
    db_file = os.path.join('..', '..', 'data', 'processed', 'city_claims.db')
    load_csv_to_db(csv_file, db_file)
