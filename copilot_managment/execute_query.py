from sqlalchemy import create_engine,text



REAL_DB_USER = "postgres"
REAL_DB_PASSWORD = "test"
REAL_DB_HOST = "localhost"
REAL_DB_NAME = "postgres"
REAL_DB_PORT = "5431"



# Create engines for both databases
real_engine = create_engine(
    f"postgresql+psycopg2://{REAL_DB_USER}:{REAL_DB_PASSWORD}@{REAL_DB_HOST}:{REAL_DB_PORT}/{REAL_DB_NAME}"
)
def execute_real_sql_query(sql_query):
   
    with real_engine.connect() as connection:
        result = connection.execute(text(sql_query))
        return result.fetchall()
    

# sql_query='SELECT COUNT(*) FROM "Customers" '
# print(execute_real_sql_query(sql_query))