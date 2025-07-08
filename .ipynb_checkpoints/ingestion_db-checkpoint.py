import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

engine = create_engine('sqlite:///inventory.db')

def load_raw_data():
    '''This function will load the CSVs as dataframe and ingest into db'''
    start = time.time()
    logging.info('Starting data ingestion process...')
    
    if not os.path.exists('dataset'):
        logging.error('Dataset directory does not exist')
        return
    
    csv_files = [f for f in os.listdir('dataset') if f.endswith('.csv')]
    if not csv_files:
        logging.warning('No CSV files found in dataset directory')
        return
    
    logging.info(f'Found {len(csv_files)} CSV files to process')
    
    for file in csv_files:
        logging.info(f'Starting to process file: {file}')
        try:
            chunk_size = 20000 
            table_name = file[:-4]
            
            total_rows = 0
            for chunk_number, chunk in enumerate(pd.read_csv(f'dataset/{file}', chunksize=chunk_size)):
                print(f"Processing {file}, chunk {chunk_number}, shape: {chunk.shape}")
                
                if_exists = 'replace' if chunk_number == 0 else 'append'
                chunk.to_sql(table_name, engine, if_exists=if_exists, index=False)
                total_rows += len(chunk)
            
            logging.info(f"Completed processing {file} - Total rows: {total_rows}")
            print(f"Completed processing {file} - Total rows: {total_rows}")
            
        except Exception as e:
            logging.error(f"Error processing file {file}: {str(e)}")
            print(f"Error processing file {file}: {str(e)}")
    
    end = time.time()
    total_time = (end - start) / 60
    logging.info('-------------Ingestion Complete------------')
    logging.info(f'Total Time Taken: {total_time:.2f} minutes')
    print(f'Total Time Taken: {total_time:.2f} minutes')

if __name__ == '__main__': 
    load_raw_data()