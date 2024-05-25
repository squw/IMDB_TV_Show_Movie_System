import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote

# Create a password.env to store password: file has one line: PASSWORD = "your_password"
# This line loads the env file created
load_dotenv(r'C:\Users\squw-\My Drive\uWaterloo\CS 338\Final Project\password.env')

# MySQL Creds, change to your own if necessary
host = "localhost"
username = "root"
password = os.getenv('MY_PASSWORD')
database_name = "imdb_data"


# Tables to add
table_names = ["name_basics", "title_akas", "title_basics", "title_crew", "title_episode", "title_pricipals", "title_ratings"]
# Paths for the tsv files
file_paths = [r"your_path_to_name.basics.tsv", 
              r"your_path_to_title.akas.tsv", 
              r"your_path_to_title.basics.tsv", 
              r"your_path_to_title.crew.tsv", 
              r"your_path_to_title.episode.tsv", 
              r"your_path_to_title.principals.tsv", 
              r"your_path_to_title.ratings.tsv"]

# Function to load table given the table name and the TSV file path
def load_table(table_name, file_path): 
    # Read the TSV file (limiting 100 lines for faster testing speed)
    df = pd.read_csv(file_path, sep='\t', na_values='\\N', nrows=100)

    # Replace NaN with None for SQL NULL values
    df = df.where(pd.notnull(df), None)

    # Create SQLAlchemy engine
    engine = create_engine(f"mysql+pymysql://{quote(username)}:{quote(password)}@{quote(host)}/{quote(database_name)}?charset=utf8mb4")

    # Load the DataFrame into the MySQL table
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    
for i in range(len(table_names)): 
    load_table(table_names[i], file_paths[i])