import base64
import json
from io import StringIO
from json import JSONDecodeError


import requests
import streamlit as st
from PIL import Image
from requests import Response

backend_url = "http://backend:8000/v1/mission-success/"

st.title("Never Tell Mee Odds")
#st.markdown("<h2 style='text-align: center; color: white;'>Never Tell Me The Odds</h2>", unsafe_allow_html=True)
#st.markdown("<h1 style='text-align: center; color: white;'>Never Tell Me The Odds</h1>", unsafe_allow_html=True)


mid_column_left, mid_column_right = st.columns(2)
st.text("")
gif = open("gif/never-tell-me-the-odds.gif", "rb")
contents = gif.read()
data_url = base64.b64encode(contents).decode("utf-8")
gif.close()
st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="gif">',unsafe_allow_html=True)
st.text("")
st.text("")
st.text("")
top_column_left, top_column_right = st.columns(2)
top_column_left.subheader("Save the Galaxy !")
st.write("Quick !! Upload a JSON file of the data intercepted by the rebels before it's too late ")

uploaded_file = st.file_uploader(
    label="",
    type=["json"],
    key="file_uploader",
)
 
mid_column_left, mid_column_right = st.columns(2)
if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    try:
        json_input = json.loads(string_data)
        result = requests.post(url=backend_url, json=json_input)
        mid_column_right.header(f"{int(result.content)} %")
                 
    except JSONDecodeError as jde:
        st.error("Invalid JSON file format. Please make sure you follow the instructions given on https://github.com/lioncowlionant/developer-test ")



