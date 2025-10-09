import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class VectorSearchUtils:
    def __init__(self):
        # No external API needed - using Oracle's built-in vector embedding
        pass
    
    def search_similar_quotes(self, db_connection, search_text, top_k=10):
        """Search for similar movie quotes using Oracle's native vector similarity"""
        try:
            # SQL query using Oracle's VECTOR_EMBEDDING function and VECTOR_DISTANCE
            # This is exactly like your example query but parameterized
            query = """
            SELECT 
                VECTOR_DISTANCE(MOVIE_QUOTE_VECTOR, 
                    (VECTOR_EMBEDDING(all_minilm_l12_v2 USING :search_text AS data))
                ) as distance,
                MOVIE,
                MOVIE_QUOTE,
                MOVIE_TYPE,
                MOVIE_YEAR
            FROM DEV.MOVIE_QUOTES
            ORDER BY 1
            FETCH APPROXIMATE FIRST :top_k ROWS ONLY
            """
            
            # Execute query with parameters
            results = db_connection.execute_query(
                query, 
                {
                    'search_text': search_text,
                    'top_k': top_k
                }
            )
            
            if results:
                columns = ['DISTANCE', 'MOVIE', 'MOVIE_QUOTE', 'MOVIE_TYPE', 'MOVIE_YEAR']
                return results, columns
            
            return None, None
            
        except Exception as e:
            st.error(f"Vector search failed: {str(e)}")
            return None, None
    
    def search_movie_quotes_by_text(self, db_connection, search_text, search_type="both"):
        """Search movie quotes using traditional text search"""
        try:
            search_term = f"%{search_text.upper()}%"
            
            if search_type == "movie":
                query = """
                SELECT MOVIE, MOVIE_QUOTE, MOVIE_TYPE, MOVIE_YEAR
                FROM DEV.MOVIE_QUOTES
                WHERE UPPER(MOVIE) LIKE :search_term
                ORDER BY MOVIE, MOVIE_YEAR
                """
            elif search_type == "quote":
                query = """
                SELECT MOVIE, MOVIE_QUOTE, MOVIE_TYPE, MOVIE_YEAR
                FROM DEV.MOVIE_QUOTES
                WHERE UPPER(MOVIE_QUOTE) LIKE :search_term
                ORDER BY MOVIE, MOVIE_YEAR
                """
            else:  # both
                query = """
                SELECT MOVIE, MOVIE_QUOTE, MOVIE_TYPE, MOVIE_YEAR
                FROM DEV.MOVIE_QUOTES
                WHERE UPPER(MOVIE) LIKE :search_term 
                   OR UPPER(MOVIE_QUOTE) LIKE :search_term
                ORDER BY MOVIE, MOVIE_YEAR
                """
            
            results = db_connection.execute_query(query, {'search_term': search_term})
            
            if results:
                columns = ['MOVIE', 'MOVIE_QUOTE', 'MOVIE_TYPE', 'MOVIE_YEAR']
                return results, columns
            
            return None, None
            
        except Exception as e:
            st.error(f"Text search failed: {str(e)}")
            return None, None
    
    def get_random_quotes(self, db_connection, limit=5):
        """Get random movie quotes for demonstration"""
        try:
            query = """
            SELECT MOVIE, MOVIE_QUOTE, MOVIE_TYPE, MOVIE_YEAR
            FROM DEV.MOVIE_QUOTES
            ORDER BY DBMS_RANDOM.VALUE
            FETCH FIRST :limit ROWS ONLY
            """
            
            results = db_connection.execute_query(query, {'limit': limit})
            
            if results:
                columns = ['MOVIE', 'MOVIE_QUOTE', 'MOVIE_TYPE', 'MOVIE_YEAR']
                return results, columns
            
            return None, None
            
        except Exception as e:
            st.error(f"Failed to get random quotes: {str(e)}")
            return None, None