"""
Complete ETL Pipeline Example
Demonstrates best practices for data engineering with Docker
"""

import pandas as pd
from sqlalchemy import create_engine
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ETLPipeline:
    """ETL Pipeline for processing CSV data to PostgreSQL"""
    
    def __init__(self):
        self.input_path = os.getenv('INPUT_CSV', '/data/sample_data.csv')
        self.table_name = os.getenv('TABLE_NAME', 'processed_data')
        self.db_url = os.getenv('DATABASE_URL')
        
        if not self.db_url:
            raise ValueError("DATABASE_URL environment variable is required")
        
        self.engine = None
        
    def extract(self):
        """Extract data from CSV file"""
        logger.info(f"Extracting data from {self.input_path}")
        
        try:
            df = pd.read_csv(self.input_path)
            logger.info(f"Successfully extracted {len(df)} rows")
            return df
        except FileNotFoundError:
            logger.error(f"File not found: {self.input_path}")
            raise
        except Exception as e:
            logger.error(f"Error reading CSV: {str(e)}")
            raise
    
    def transform(self, df):
        """Transform the data"""
        logger.info("Starting data transformation")
        
        initial_rows = len(df)
        
        # Add metadata columns
        df['processed_at'] = datetime.now()
        df['pipeline_version'] = '1.0'
        
        # Data quality checks
        logger.info("Performing data quality checks...")
        
        # Remove duplicates
        df = df.drop_duplicates()
        duplicates_removed = initial_rows - len(df)
        if duplicates_removed > 0:
            logger.warning(f"Removed {duplicates_removed} duplicate rows")
        
        # Remove rows with missing values
        df = df.dropna()
        na_removed = initial_rows - duplicates_removed - len(df)
        if na_removed > 0:
            logger.warning(f"Removed {na_removed} rows with missing values")
        
        # Data transformations (example)
        if 'value' in df.columns:
            df['value_doubled'] = df['value'] * 2
            df['value_category'] = df['value'].apply(self._categorize_value)
        
        logger.info(f"Transformation complete. {len(df)} rows remain")
        return df
    
    def _categorize_value(self, value):
        """Helper function to categorize values"""
        if value < 100:
            return 'Low'
        elif value < 200:
            return 'Medium'
        else:
            return 'High'
    
    def load(self, df):
        """Load data to PostgreSQL"""
        logger.info(f"Loading data to table: {self.table_name}")
        
        try:
            # Create database engine
            self.engine = create_engine(self.db_url)
            
            # Load data
            df.to_sql(
                self.table_name,
                self.engine,
                if_exists='replace',
                index=False,
                method='multi',
                chunksize=1000
            )
            
            logger.info(f"Successfully loaded {len(df)} rows to {self.table_name}")
            
            # Verify load
            verify_query = f"SELECT COUNT(*) FROM {self.table_name}"
            with self.engine.connect() as conn:
                result = conn.execute(verify_query)
                count = result.scalar()
                logger.info(f"Verification: {count} rows in database")
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
        finally:
            if self.engine:
                self.engine.dispose()
    
    def run(self):
        """Execute the complete ETL pipeline"""
        logger.info("=" * 60)
        logger.info("Starting ETL Pipeline")
        logger.info("=" * 60)
        
        start_time = datetime.now()
        
        try:
            # Extract
            df = self.extract()
            
            # Transform
            df = self.transform(df)
            
            # Load
            self.load(df)
            
            # Calculate duration
            duration = (datetime.now() - start_time).total_seconds()
            
            logger.info("=" * 60)
            logger.info(f"ETL Pipeline completed successfully in {duration:.2f} seconds")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error("=" * 60)
            logger.error(f"ETL Pipeline failed: {str(e)}")
            logger.error("=" * 60)
            return False


def main():
    """Main entry point"""
    pipeline = ETLPipeline()
    success = pipeline.run()
    
    # Exit with appropriate code
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
