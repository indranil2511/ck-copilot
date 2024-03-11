import streamlit as st
from langchain_openai import OpenAI
from typing import Dict, Any 
from query_utils import *
from prompt import *
import pandas as pd
from sql_to_natural import *
import os
from dotenv import load_dotenv

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

def get_prompt():
    # st.title('Data Extractor Copilot CK')
    # prompt = st.chat_input("Ask me...")
    
    prompt = st.chat_input("What do you wanna know?")
    # query_arr.append(prompt)
    # for row in query_arr:
    #     print(row)
    #     st.sidebar.write(
    #         f'<span class="chat-items">{row}</span>',
    #         unsafe_allow_html=True,
    #     )
    on_chat_submit(prompt)
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
    


def on_chat_submit(chat_input):
    """
    Function to handle user input and generate responses.
    """
    # if not chat_input:
    #     st.warning("Please enter a valid input.")
    #     st.stop()
    
    if chat_input:
        sql_query=None
        try:
            if chat_input.lower() == "hi elsa":
                response = "I am Elsa, a bot designed to help with managing tasks related to product shipment. How can I assist you?"
                st.session_state.history.append({"role": "user", "content": chat_input})
                st.session_state.history.append({"role": "assistant", "content": response})
            else:
                st.session_state.conversation_history.append({"role": "user", "content": chat_input})
                sql_query = get_sql_query(QUERY.format(question=chat_input))
                print(sql_query)
                
            if sql_query:
                MAX_RESULTS = 100
                if os.environ['DEBUG'] == True:
                    st.success("Generated SQL query:")
                    st.code(sql_query, language="sql")

                try:
                    output = execute_real_sql_query(sql_query)
                    
                    print(output)
                    if output is not None:
                        #   st.write("Query Results:")
                        if len(output) > MAX_RESULTS:
                            st.warning(f"Displaying only the first {MAX_RESULTS} results.")
                            output = output[:MAX_RESULTS]

                        print(os.environ['DEBUG'])
                        if os.environ['DEBUG'] == True:
                            st.dataframe(output)  # Display results as a DataFrame
                        
                        natural_prompt = combine_prompt_data(chat_input, output)
                        llm_output = process_with_llm(natural_prompt)
                        llm_output = llm_output.replace("The data reveals that", "")
                        llm_output = llm_output.replace("The data suggests that", "")
                        llm_output = llm_output.replace("The data shows that", "")
                        llm_output = llm_output.replace("The data indicates that", "")

                        # Append assistant's reply to the conversation history
                        st.session_state.conversation_history.append({"role": "assistant", "content": llm_output})
                        #st.chat_message(llm_output)

                        # Update the Streamlit chat history
                        if "history" in st.session_state:
                            st.session_state.history.append({"role": "user", "content": chat_input})
                            st.session_state.history.append({"role": "assistant", "content": llm_output})
                    else:
                        st.info("The query did not return any results.")
                except Exception as e:
                    st.error(f"An error occurred while executing the query: {e}")
            else:
                st.write(" ")
                # st.write("I am Elsa, a bot designed to help with managing tasks related to product shipment. I am not programmed to answer such questions or provide information on this. How can I assist you?")
                # st.write("Failed to generate SQL query.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

