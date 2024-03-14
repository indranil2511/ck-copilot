from langchain_openai import OpenAI
import os
from dotenv import load_dotenv
import openai
# import streamlit as st
import pandas as pd

from copilot import *

load_dotenv()
# Replace with your OpenAI API key
api_key = os.environ['API_KEY']
llm = OpenAI(temperature=0, openai_api_key=api_key)

def process_with_llm(prompt, data):
    df = pd.DataFrame(data) 

    # Convert dataframe to a human-readable format (e.g., CSV)
    df_string = df.to_csv(index=False)

    # Craft a comprehensive prompt
    llm_prompt = f"""
    I have been given a question: {prompt}. The answer for this question is provided in a table format below:

    **Table:**

    {df_string}
    Can you summarize this information in a natural language format that directly answers the question? 
    Avoid phrasing that suggests the data came from a table (e.g., "This data shows").

    For example, if the question is "What is sales?", the answer should be a straightforward statement like "Sales is 'xx'."
    """
    
    a=llm.generate([llm_prompt], max_tokens = 200, temperature=0)
    # Extract the generated text from the response
    summary = a.generations[0][0].text
    return summary

