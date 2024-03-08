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

def combine_prompt_data(prompt, data):
    df = pd.DataFrame(data)

    # Convert the DataFrame to a human-readable format (e.g., CSV)
    df_string = df.to_csv(index=False)

    natural_prompt = "**Prompt:** {prompt}\n\n" + df_string
    return natural_prompt

def process_with_llm(natural_prompt):

    # Craft a comprehensive prompt
    llm_prompt = f"I have been given a question and a dataframe which is answer of the asked question: \n {natural_prompt} \n  Please provide a concise summary of the key insights or trends in the data in natural language. concise the answer with less words as less you can do"
    # llm_prompt = f"Please provide a brief summary highlighting the main trends or insights in the data, focusing on the top-selling products and customer preferences.\n\n{natural_prompt}"

    # st.write(combined_content)
    a=llm.generate([llm_prompt],max_tokens=100,temperature=0.5)
    # print(a)
    # Extract the generated text from the response
    summary = a.generations[0][0].text
    # st.write(summary)
    return summary

# Example usage
# user_prompt = "Give me products which are ordered more than once"
# user_dataframe = pd.DataFrame({
#     "Product_Id": ["2001-6158-8095", "2742-5936-3491", "1234-5678-9012"],
#     "Product Name": ["Notebook Cover", "Desk Organizer", "Headphones"],
#     "Product_Category": ["Material", "Electronics", "Electronics"],
#     "Price": [145.75, 199.99, 79.99]
# })
# def write_to_file(prompt, sql_output, file_path):
#     with open(file_path, "w") as file:
#         file.write(f"**Prompt:** {prompt}\n\n")
#         file.write(f"**SQL Output:**\n\n{sql_output.to_markdown(index=False)}")

# combine_prompt_data(user_prompt, user_dataframe)


# llm_output = process_with_llm("combined_prompt_data.txt")
# print(llm_output)

