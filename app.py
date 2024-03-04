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

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Copilot",
        page_icon="images/at1r90gg7joulymfg2qe.webp",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inject custom CSS for glowing border effect
    st.markdown(
        """
        <style>
        .cover-glow {
            width: 100%;
            height: auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Load and display sidebar image with glowing effect
    img_path = "images/ck-logo.webp"
    img_base64 = img_to_base64(img_path)
    st.sidebar.markdown(
        f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
        unsafe_allow_html=True,
    )

    st.markdown(
    """
    <style>
        /* CSS to change the sidebar color */
        .st-emotion-cache-vk3wp9 {
            background-color: #000000ed; /* Change this color to your desired color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.write("# Welcome to CK Copilot! 👋")

    get_prompt()
    # st.chat_input("Ask me about Streamlit updates:")

# Function to convert image to base64
def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode() 
    

from app import run

if __name__ == "__main__":
    run()
