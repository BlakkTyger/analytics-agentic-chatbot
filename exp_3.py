import pandas as pd
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, inspect
import os
from dotenv import load_dotenv
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from typing import List, Dict
import glob

load_dotenv()

OPENAI_KEY = os.environ["OPENAI_KEY"]

class MultiDataFrameAgent:
    def __init__(self, csv_directory: str):
        """
        Initialize the agent with a directory containing CSV files.
        
        Args:
            csv_directory (str): Path to directory containing CSV files
        """
        self.csv_directory = csv_directory
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_KEY)
        self.engine = create_engine("sqlite:///multi_df.db")
        self.loaded_tables: Dict[str, List[str]] = {}  # Keep track of loaded tables and their columns
        
    def load_all_csvs(self) -> None:
        """Load all CSV files from the directory and store their schema information."""
        csv_files = glob.glob(os.path.join(self.csv_directory, "*.csv"))
        
        for csv_path in csv_files:
            df = pd.read_csv(csv_path)
            table_name = os.path.splitext(os.path.basename(csv_path))[0]
            df.to_sql(table_name, self.engine, index=False, if_exists='replace')
            self.loaded_tables[table_name] = list(df.columns)
            
    def get_relevant_tables(self, query: str) -> List[str]:
        """
        Analyze the query and determine which tables are relevant.
        
        Args:
            query (str): The user's query
            
        Returns:
            List[str]: List of relevant table names
        """
        # Create a prompt to analyze which tables are needed
        table_info = "\n".join([
            f"Table: {table}\nColumns: {', '.join(columns)}"
            for table, columns in self.loaded_tables.items()
        ])
        
        analysis_prompt = f"""
        Given the following tables and their columns:
        {table_info}
        
        And the user query: "{query}"
        
        Which tables are needed to answer this query? Respond with just the table names separated by commas, or 'NONE' if no tables are relevant.
        Consider:
        1. Column names that match query terms
        2. Table names that match query context
        3. Related tables that might need to be joined
        """
        
        response = self.llm.invoke(analysis_prompt)
        relevant_tables = [table.strip() for table in response.content.split(',') if table.strip() in self.loaded_tables]
        
        return relevant_tables if relevant_tables else []
    
    def execute_query(self, query: str) -> str:
        """
        Execute the query using the relevant tables.
        
        Args:
            query (str): The user's query
            
        Returns:
            str: The query result
        """
        # First, ensure all CSVs are loaded
        self.load_all_csvs()
        
        # Get relevant tables
        relevant_tables = self.get_relevant_tables(query)
        
        if not relevant_tables:
            return "No relevant tables found to answer this query."
        
        db = SQLDatabase(engine=self.engine)
        
        agent_executor = create_sql_agent(
            self.llm,
            db=db,
            agent_type="openai-tools",
            verbose=True
        )
        
        result = agent_executor.invoke({"input": query})
        
        return result["output"]

def main():
    agent = MultiDataFrameAgent("data")
    query = "Do a time series analysis of the products sold"
    result = agent.execute_query(query)
    print(f"Query: {query}")
    print(f"Result: {result}")

if __name__ == "__main__":
    main()