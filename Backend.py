from fastapi import FastAPI
from pydantic import BaseModel
from main import *
import shutil
import os
from dotenv import load_dotenv
# Create the FastAPI app
app = FastAPI()
load_dotenv()
from pydantic import BaseModel

Dataframe =MultiDataFrameAgent("data")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}

@app.post("/api/upload_csv")
def upload_csv():
    """
    Upload a CSV file to the backend and add it to the data folder.
    
    Args:
        csv_path (str): Path to the CSV file
    
    Returns:
        str: Success message
    """
    Dataframe.load_all_csvs()
    
    return "CSV file uploaded and added to the data folder successfully."

class QueryRequest(BaseModel):
    query: str

@app.post("/api/query")
def query(request: QueryRequest):
    """
    Query the loaded CSV files based on the user's query.
    
    Args:
        request (QueryRequest): Request body containing the query
    
    Returns:
        List[str]: Relevant table names
    """
    response = Dataframe.execute_query(request.query)
    return response
