import streamlit as st
import pandas as pd
import requests  # For calling the backend API
import uuid  # For generating unique filenames
# Streamlit app setup
st.title("Analytics and Insights Agentic Chatbot")

# Upload CSV file
st.header("Upload a CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
backend_url = "http://localhost:8000"
# Display uploaded CSV file
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of Uploaded CSV:")
        st.write(df.head())
        # Save the file to the data folder
        filePath = "data/uploaded_file_{uuid.uuid4()}.csv"
        df.to_csv(filePath, index=False)
        # Send the filename to the backend
        
        try:
            response = requests.post(backend_url+"/api/upload_csv")
            if response.status_code == 200:
                st.success("Filename successfully sent to the backend.")
            else:
                st.error(f"Backend returned an error: {response.status_code}")
        except Exception as e:
            st.error(f"Error communicating with the backend: {e}")
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
        # Backend API callL
        try:
            response = requests.post(backend_url+"/api/query", json={"query": user_query})
            if response.status_code == 200:
                st.success("Response from Backend:")
                st.write(response.json())
            else:
                st.error(f"Backend returned an error: {response.status_code}")
        except Exception as e:
            st.error(f"Error communicating with the backend: {e}")
