import streamlit as st
from dotenv import load_dotenv
import os

st.write ("Welcome to our App")
st.write ("This is a tool to help you book your business trip")

st.write (""" Please enter your departure place, destination office and start date to get started. 
          We'll show you your flight options. """)

# How to load data from .env file
load_dotenv()
 api_key = os.getenv("API_KEY")
