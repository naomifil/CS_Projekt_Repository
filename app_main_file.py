import streamlit as st
from dotenv import load_dotenv
import os

st.write ("Welcome to our App")
st.write ("This is a tool to help you book your business trip")

st.write ("Please enter your destination to get started")

# How to load data from .env file
load_dotenv()
 api_key = os.getenv("API_KEY")
