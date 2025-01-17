# Analytics and Insights Agentic Chatbot

We built an **Low Latency** **Agentic** ChatBot which conducts custom Analytics and provides insights to companies on the basis of the tables provided by them.

## Data Input: Google Drive Connector
In order to input the data tables, the user can either upload the excel or csv files, or **connect to their Google Drive Account**. We will automatically fetch all the csv files and tables from the user's account in order to conduct analytics on them. For future developments, we can also integrate other input connectors such as AirTable, OneDrive, Kafka, Company Databases etc in order to allow for seamless integration.

## SQL Agent for Insights and Analytics
An **SQL Agent** is develop using LangChain, which can query the data in order to derive useful insights. It can also conduct analytics using OpenAI's in-built tool calling. The workflow is as follows:
1. Tables inputted by the user are converted into SQL databases.
2. Tables which are relevant to the query are decided by analyzing the information in the files, such as column headers.
3. Relevant Data from relevant tables is extracted by the **SQL Agent**
4. Using **Agent Executor**, data analytics are conducted on the basis of the data fetched from the tables. 
5. According to the fetched data and analyzed data, the agent collates a **actionable insights** which are shown to the user.

## Additional Features
- Seamless Integration possible, as the codebase is highly modular and can be simply accessed via certain API endpoints. It can be **intergrated  into any dashboard** as a simplt ChatBot.
- Conversational AI capabilities added by integrating OpenAI GPT-4o-mini. For future purposes, chat history could be added to retain memory of previous chats.
- Solution can be **scaled** for large number of files and large tables, providing an industry standard solution.
- Security can be ensured by integrating OpenLLMs in future.

