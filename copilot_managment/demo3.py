from langchain_openai import OpenAI
# from helper import *
import streamlit as st
from typing import Dict, Any 
from execute_query import *
from prompt import *

 
# Your OpenAI API key
API_KEY = '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'
 
llm = OpenAI(temperature=0, openai_api_key=API_KEY)

def get_sql_query(prompt):
    """
    Get SQL query from the language model based on the enhanced prompt, without connecting to the database.
    """
    prompt_list = [prompt]
    generations = llm.generate(prompt_list)
    return generations.generations[0][0].text


def get_prompt():
    st.title('Data Extractor Copilot CK')
    prompt = st.text_area("What do you wanna know?")
    if prompt:
        try:
            sql_query = get_sql_query(QUERY.format(question=prompt))
            if sql_query:
                st.success("Generated SQL query:")
                st.code(sql_query, language="sql")

                try:
                    output = execute_real_sql_query(sql_query)
                    if output is not None:
                        #   st.write("Query Results:")
                        st.dataframe(output)  # Display results as a DataFrame
                    else:
                        st.info("The query did not return any results.")
                except Exception as e:
                    st.error(f"An error occurred while executing the query: {e}")
            else:
                st.write("Failed to generate SQL query.")

        except Exception as e:
            st.error(f"An error occurred: {e}") 

get_prompt()