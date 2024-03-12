from sqlalchemy import create_engine,text, MetaData, Table, Column, Integer, String, DateTime
from datetime import datetime
import psycopg2



REAL_DB_USER = "postgres"
REAL_DB_PASSWORD = "test"
REAL_DB_HOST = "localhost"
REAL_DB_NAME = "postgres"
REAL_DB_PORT = "5431"



# Create engines for both databases
real_engine = create_engine(
    f"postgresql+psycopg2://{REAL_DB_USER}:{REAL_DB_PASSWORD}@{REAL_DB_HOST}:{REAL_DB_PORT}/{REAL_DB_NAME}"
)
# def execute_real_sql_query(sql_query):
    
#     with real_engine.connect() as connection:
       
#             result = connection.execute(text(sql_query))
#             return result.fetchall()

def execute_real_sql_query(sql_query):
 
    with real_engine.connect() as connection:
        is_select = sql_query.strip().upper().startswith("SELECT")
        result = connection.execute(text(sql_query))
 
        if is_select:
            return result.fetchall()  # Fetch results for SELECT queries
        # else:
        #     connection.commit()  # Commit changes for DML queries
 
        return None  # Indicate successful execution without results
    


# DB_USER = "postgres"
# DB_PASSWORD = "test"
# DB_HOST = "localhost"
# DB_NAME = "postgres"
# DB_PORT = "5431"

# Establish a connection to the database
connection = psycopg2.connect(
    dbname=REAL_DB_NAME,
    user=REAL_DB_USER,
    password=REAL_DB_PASSWORD,
    host=REAL_DB_HOST,
    port=REAL_DB_PORT
)

# Create a cursor object
cursor = connection.cursor()



# Create the conversation table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS chat_history (
    id SERIAL PRIMARY KEY,
    session_id integer,
    question TEXT,
    answer TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

);
"""
cursor.execute(create_table_query)
connection.commit()