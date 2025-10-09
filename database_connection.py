import cx_Oracle
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to Oracle database"""
        try:
            # Get connection parameters from environment variables
            db_user = os.getenv('DB_USER')
            db_password = os.getenv('DB_PASSWORD')
            db_host = os.getenv('DB_HOST')
            db_port = os.getenv('DB_PORT', '1521')
            db_service_name = os.getenv('DB_SERVICE_NAME')
            
            if not all([db_user, db_password, db_host, db_service_name]):
                raise ValueError("Missing database connection parameters in .env file")
            
            # Create DSN (Data Source Name) for cx_Oracle
            dsn = cx_Oracle.makedsn(db_host, db_port, service_name=db_service_name)
            
            # Establish connection
            self.connection = cx_Oracle.connect(
                user=db_user,
                password=db_password,
                dsn=dsn,
                encoding="UTF-8"
            )
            
            self.cursor = self.connection.cursor()
            return True
            
        except Exception as e:
            st.error(f"Database connection failed: {str(e)}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except Exception as e:
            st.error(f"Error closing connection: {str(e)}")
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            if not self.connection:
                if not self.connect():
                    return None
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            return self.cursor.fetchall()
            
        except Exception as e:
            st.error(f"Query execution failed: {str(e)}")
            return None
    
    def get_column_names(self, query):
        """Get column names from cursor description"""
        try:
            if self.cursor and self.cursor.description:
                return [col[0] for col in self.cursor.description]
            return []
        except Exception as e:
            st.error(f"Error getting column names: {str(e)}")
            return []