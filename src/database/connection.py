from typing import Optional
import os
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase

# Load environment variables
load_dotenv()

class DatabaseConnection:
    _instance: Optional[SQLDatabase] = None

    @classmethod
    def get_instance(cls) -> SQLDatabase:
        """Get or create a database connection instance"""
        if cls._instance is None:
            connection_string = (
                f"mysql+pymysql://{os.getenv('db_user')}:{os.getenv('db_password')}"
                f"@{os.getenv('db_host')}/{os.getenv('db_name')}"
            )
            cls._instance = SQLDatabase.from_uri(connection_string)
        return cls._instance

    @classmethod
    def get_table_info(cls) -> str:
        """Get information about database tables"""
        return cls.get_instance().get_table_info() 