from chat_history_model import Chat_history
from sqlalchemy import create_engine,text, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import psycopg2
from sqlalchemy.orm import sessionmaker

# Create a base class for our ORM models
Base = declarative_base()

REAL_DB_USER = "ueuocca0lgifk6"
REAL_DB_PASSWORD = "pb30d343bd7c66ae728459036a59c29f07e335c178174477f65afec9a44945499"
REAL_DB_HOST = "ceu9lmqblp8t3q.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com"
REAL_DB_NAME = "d6a1qf193655v2"
REAL_DB_PORT = "5432"

# Create engines for both databases
# real_engine=psycopg2.connect(
#     dbname=REAL_DB_NAME,
#     user=REAL_DB_USER,
#     password=REAL_DB_PASSWORD,
#     host=REAL_DB_HOST,
#     port=REAL_DB_PORT
# )
real_engine = create_engine(
    # f"postgres://ueuocca0lgifk6:pb30d343bd7c66ae728459036a59c29f07e335c178174477f65afec9a44945499@ceu9lmqblp8t3q.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d6a1qf193655v2"
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
    
def update_chat_history(session_id, chat_input, llm_output):
    try:
        Base.metadata.create_all(real_engine)

        # Create a sessionmaker to interact with the database
        Session = sessionmaker(bind=real_engine)

        # Create a session
        session = Session()

        # Create a new User instance with the data you want to insert
        new_chat = Chat_history(session_id=session_id, user_id='h328ed82', question=chat_input, answer=llm_output, timestamp= datetime.now())

        # Add the new_user instance to the session
        session.add(new_chat)

        # Commit the session to execute the INSERT query
        session.commit()

        # Close the session
        session.close()

    except Exception as e:
        print(e)

def get_chat_history(user_id):
    try:
       query = """SELECT question FROM (SELECT 
                    *,
                    ROW_NUMBER() OVER (PARTITION BY session_id ORDER BY question) AS row_num
                    FROM public.chat_history
                ) AS subquery
                WHERE row_num = 1 and user_id = '%s';
                """ % (user_id)
       print(query)
       result = execute_real_sql_query(query)
       print(result)
       return result
            
    except Exception as e:
        print(e)


    


# DB_USER = "postgres"
# DB_PASSWORD = "test"
# DB_HOST = "localhost"
# DB_NAME = "postgres"
# DB_PORT = "5431"

# Establish a connection to the database
# connection = psycopg2.connect(
#     dbname=REAL_DB_NAME,
#     user=REAL_DB_USER,
#     password=REAL_DB_PASSWORD,
#     host=REAL_DB_HOST,
#     port=REAL_DB_PORT
# )

# # Create a cursor object
# cursor = connection.cursor()



# # Create the conversation table if it doesn't exist
# create_table_query = """
# CREATE TABLE IF NOT EXISTS chat_history (
#     id SERIAL PRIMARY KEY,
#     session_id integer,
#     question TEXT,
#     answer TEXT,
#     timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

# );
# """
# cursor.execute(create_table_query)
# connection.commit()