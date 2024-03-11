# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import base64
from copilot import get_prompt
from layout import load

LOGGER = get_logger(__name__)


def run():

    load()

    initial_bot_message = "Hello! I'm Elsa. How can I assist you?\n"

    if "history" not in st.session_state:
        st.session_state.history = []
        st.session_state.history.append({"role": "assistant", "content": initial_bot_message})
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    

    get_prompt()
    # st.chat_input("Ask me about Streamlit updates:")

# Function to convert image to base64
def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode() 
    

from Chat import run

if __name__ == "__main__":
    run()
