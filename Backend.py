from fastapi import FastAPI
from pydantic import BaseModel
from exp_3 import *
import shutil
import os
from dotenv import load_dotenv
# Create the FastAPI app
app = FastAPI()
load_dotenv()

Dataframe =MultiDataFrameAgent("data")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}

@app.post("/api/upload_csv")
def upload_csv(csv_path: str):
    """
    Upload a CSV file to the backend and add it to the data folder.
    
    Args:
        csv_path (str): Path to the CSV file
    
    Returns:
        str: Success message
    """
    Dataframe.load_all_csvs()
    
    return "CSV file uploaded and added to the data folder successfully."

@app.post("/api/query")
def query(query: str):
    """
    Query the loaded CSV files based on the user's query.
    
    Args:
        query (str): User's query
    
    Returns:
        List[str]: Relevant table names
    """
    response = Dataframe.execute_query(query)
    return response

