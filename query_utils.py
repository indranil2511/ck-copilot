from sqlalchemy import create_engine,text
import psycopg2



REAL_DB_USER = "postgres"
REAL_DB_PASSWORD = "rony170891"
REAL_DB_HOST = "localhost"
REAL_DB_NAME = "postgres"
REAL_DB_PORT = "5432"



# Create engines for both databases
real_engine = create_engine(
    f"postgresql+psycopg2://{REAL_DB_USER}:{REAL_DB_PASSWORD}@{REAL_DB_HOST}:{REAL_DB_PORT}/{REAL_DB_NAME}"
)
def execute_real_sql_query(sql_query):
    # Fetch database schema
    # schema_info = get_schema_info()
    # for row in schema_info:
    #     print(row)
    with real_engine.connect() as connection:
        result = connection.execute(text(sql_query))
        return result.fetchall()
    

def get_schema_info():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=REAL_DB_NAME,
        user=REAL_DB_USER,
        password=REAL_DB_PASSWORD,
        host=REAL_DB_HOST,
        port=REAL_DB_PORT
    )
    
    # Create a cursor object
    cur = conn.cursor()
    
    # Query to retrieve schema information
    query = """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public';
    """
    
    # Execute the query
    cur.execute(query)
    
    # Fetch all rows
    rows = cur.fetchall()
    
    # Close cursor and connection
    cur.close()
    conn.close()
    
    return rows