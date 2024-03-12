import streamlit as st
from langchain_openai import OpenAI
from typing import Dict, Any 
from query_utils import *
from prompt import *
import pandas as pd
from sql_to_natural import *
import os
import re
from dotenv import load_dotenv
import random
# Your OpenAI API key

API_KEY = api_key = os.environ['API_KEY']
 
llm = OpenAI(temperature=0, openai_api_key=API_KEY)
query_arr = []

load_dotenv()
def get_sql_query(prompt):
    """
    Get SQL query from the language model based on the enhanced prompt, without connecting to the database.
    """
    prompt_list = [prompt]
    generations = llm.generate(prompt_list)
    return generations.generations[0][0].text

def generate_session_id():
    """
    Generate a session ID that remains constant throughout the session.
    """
    if "session_id" not in st.session_state:
        st.session_state.session_id = random.randint(100000, 999999)
    return st.session_state.session_id


def get_prompt():
    # st.title('Data Extractor Copilot CK')
    # prompt = st.chat_input("Ask me...")
    session_id = generate_session_id()
    prompt = st.chat_input("What do you wanna know?")
    # query_arr.append(prompt)
    # for row in query_arr:
    #     print(row)
    #     st.sidebar.write(
    #         f'<span class="chat-items">{row}</span>',
    #         unsafe_allow_html=True,
    #     )
    on_chat_submit(prompt,session_id)
    # Display chat history with custom avatars
    for message in st.session_state.history[-20:]:
        role = message["role"]
        
        # Set avatar based on role
        if role == "assistant":
            avatar_image = "images/Screenshot 2024-03-08 at 1.51.15 PM.png"
        elif role == "user":
            avatar_image = "images/user-account-management-logo-user-icon-11562867145a56rus2zwu.png"
        else:
            avatar_image = None  # Default
        
        with st.chat_message(role, avatar=avatar_image):
            st.write(message["content"])
    


def on_chat_submit(chat_input,session_id):
    """
    Function to handle user input and generate responses.
    """
    if chat_input:
        sql_query=None
        try:
            
            if chat_input.lower() == "hi elsa":
                response = "I am Elsa, a bot designed to help with managing tasks related to product shipment. How can I assist you?"
                st.session_state.history.append({"role": "user", "content": chat_input,"session_id":session_id})
                st.session_state.history.append({"role": "assistant", "content": response,"session_id":session_id})
            else:
                st.session_state.conversation_history.append({"role": "user", "content": chat_input,"session_id":session_id})
                sql_query = get_sql_query(QUERY.format(question=chat_input))
                print(sql_query)
                
            if sql_query:
                MAX_RESULTS = 100
                if os.environ['DEBUG'] == 'True':
                    st.success("Generated SQL query:")
                    st.code(sql_query, language="sql")

                try:
                    """
                    Check if the given string is an SQL query.
                    """
                    # Define a regular expression pattern to match common SQL query patterns
                    sql_pattern = r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)\b"
                    # Use the search function to find matches
                    match = re.search(sql_pattern, sql_query, re.IGNORECASE)

                    if match:
                        
                        # params = {"new_value": "new_value", "condition_value": "condition_value"}

                        output = execute_real_sql_query(sql_query)
                        # match = re.search(sql_pattern, sql_query, re.IGNORECASE)
                        print(output)
                        if output is not None:
                            if len(output) > MAX_RESULTS:
                                st.warning(f"Displaying only the first {MAX_RESULTS} results.")
                                output = output[:MAX_RESULTS]
                            #   st.write("Query Results:")
                            if os.environ['DEBUG'] == 'True':
                                st.dataframe(output)  # Display results as a DataFrame
                            
                            natural_prompt = combine_prompt_data(chat_input, output)
                            llm_output = process_with_llm(natural_prompt)
                            update_chat_history(session_id, chat_input, llm_output) 

                            # Append assistant's reply to the conversation history
                            st.session_state.conversation_history.append({"role": "assistant", "content": llm_output,"session_id":session_id})

                            # Update the Streamlit chat history
                            if "history" in st.session_state:
                                st.session_state.history.append({"role": "user", "content": chat_input,"session_id":session_id})
                                st.session_state.history.append({"role": "assistant", "content": llm_output,"session_id":session_id})
                        else:
                            if sql_query.strip().upper().startswith("UPDATE"):
                                st.warning("Updating table is not allowed!")
                            elif sql_query.strip().upper().startswith("INSERT"):
                                st.warning("Data insertion is not allowed!")
                            elif sql_query.strip().upper().startswith("DELETE"):
                                st.warning("You cannot delete data!")
                            else:
                                st.info("The query did not return any results.")
                    else:
                        if "history" in st.session_state:
                            st.session_state.history.append({"role": "user", "content": chat_input,"session_id":session_id})
                            st.session_state.history.append({"role": "assistant", "content": sql_query,"session_id":session_id})

                except Exception as e:
                    st.error(f"An error occurred while executing the query: {e}")
            else:
                st.write(" ")
                # st.write("I am Elsa, a bot designed to help with managing tasks related to product shipment. I am not programmed to answer such questions or provide information on this. How can I assist you?")
                # st.write("Failed to generate SQL query.")

        except Exception as e:
            st.error(f"An error occurred: {e}")