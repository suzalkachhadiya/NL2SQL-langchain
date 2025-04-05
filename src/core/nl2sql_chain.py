from typing import Dict, Any, List
import os
from dotenv import load_dotenv
from langchain.chains import create_sql_query_chain
from langchain_community.tools import QuerySQLDatabaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

from ..database.connection import DatabaseConnection
from ..prompts.prompt_builder import PromptBuilder

# Load environment variables
load_dotenv()

class NL2SQLChain:
    def __init__(self):
        self.db = DatabaseConnection.get_instance()
        self.prompt_builder = PromptBuilder()
        
        # Set up API keys from environment variables
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
        os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
        os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")

    def create_chain(self):
        """Create the NL2SQL chain"""
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        
        # Create the query generation chain
        generate_query = create_sql_query_chain(
            llm,
            self.db,
            self.prompt_builder.create_final_prompt().partial(top_k=2)
        )
        
        # Create the query execution tool
        execute_query = QuerySQLDatabaseTool(db=self.db)
        
        # Create the answer formatting chain
        rephrase_answer = (
            self.prompt_builder.create_answer_prompt() 
            | llm 
            | StrOutputParser()
        )
        
        # Combine all components
        chain = (
            RunnablePassthrough.assign(query=generate_query).assign(
                result=itemgetter("query") | execute_query
            )
            | rephrase_answer
        )
        
        return chain

    def process_question(self, question: str, messages: List[Dict[str, str]]) -> str:
        """
        Process a natural language question and return the response
        
        Args:
            question: The natural language question
            messages: List of previous messages in the conversation
            
        Returns:
            str: The formatted response
        """
        chain = self.create_chain()
        response = chain.invoke({
            "question": question,
            "messages": messages
        })
        return response 