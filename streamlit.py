import streamlit as st
import pandas as pd
import requests  # For calling the backend API

# Streamlit app setup
st.title("Simple Streamlit App")

# Upload CSV file
st.header("Upload a CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Display uploaded CSV file
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of Uploaded CSV:")
        st.write(df.head())
    except Exception as e:
        st.error(f"Error reading the file: {e}")

# Input for user's query
st.header("Enter Your Query")
user_query = st.text_input("Type your query here:")

# Button to send the query to the backend
if st.button("Send"):
    if not uploaded_file:
        st.error("Please upload a CSV file before sending the query.")
    elif not user_query.strip():
        st.error("Please enter a query before sending.")
    else:
        # Backend API call
        backend_url = "http://your-backend-endpoint.com/api"  # Replace with your backend URL
        try:
            response = requests.post(backend_url, json={"query": user_query})
            if response.status_code == 200:
                st.success("Response from Backend:")
                st.write(response.json())
            else:
                st.error(f"Backend returned an error: {response.status_code}")
        except Exception as e:
            st.error(f"Error communicating with the backend: {e}")
