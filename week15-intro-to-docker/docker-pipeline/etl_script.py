import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os

def main():
    print("Starting ETL process...")
    
    # Read CSV file
    print("Reading CSV file...")
    df = pd.read_csv('/data/sample_data.csv')
    print(f"Loaded {len(df)} rows")
    
    # Simple transformation
    print("Transforming data...")
    df['processed_at'] = pd.Timestamp.now()
    
    # Connect to database
    print("Connecting to database...")
    db_url = os.getenv('DATABASE_URL', 
                       'postgresql://postgres:mytestpassword@localhost:5432/dataeng_db')
    engine = create_engine(db_url)
    
    # Load to database
    print("Loading to database...")
    df.to_sql('processed_data', engine, if_exists='replace', index=False)
    
    print("ETL process completed successfully!")

if __name__ == "__main__":
    main()
