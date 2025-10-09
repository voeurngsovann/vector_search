import streamlit as st
import pandas as pd
import os
from database_connection import DatabaseConnection
from vector_search_utils import VectorSearchUtils

# Page configuration
st.set_page_config(
    page_title="Movie Quotes Vector Search",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .search-container {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .result-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f4e79;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .movie-title {
        font-weight: bold;
        color: #1f4e79;
        font-size: 1.2rem;
    }
    .quote-text {
        font-style: italic;
        color: #2c3e50;
        margin: 0.5rem 0;
    }
    .movie-info {
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    .distance-score {
        color: #e74c3c;
        font-weight: bold;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'db_connection' not in st.session_state:
        st.session_state.db_connection = None
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'connected' not in st.session_state:
        st.session_state.connected = False

def connect_to_database():
    """Connect to the Oracle database using cx_Oracle"""
    if not st.session_state.connected:
        with st.spinner("Connecting to Oracle database with cx_Oracle..."):
            st.session_state.db_connection = DatabaseConnection()
            if st.session_state.db_connection.connect():
                st.session_state.connected = True
                st.success("✅ Connected to Oracle Database successfully using cx_Oracle!")
                return True
            else:
                st.error("❌ Failed to connect to database. Please check your .env configuration.")
                return False
    return True

def display_results(results, columns, search_type="vector"):
    """Display search results in a formatted way"""
    if not results:
        st.warning("No results found for your search.")
        return
    
    # Create DataFrame
    df = pd.DataFrame(results, columns=columns)
    
    st.success(f"Found {len(results)} results:")
    
    # Display results as cards
    for idx, row in df.iterrows():
        with st.container():
            if search_type == "vector" and 'DISTANCE' in df.columns:
                # Lower distance means higher similarity
                distance_score = f" (Distance: {row['DISTANCE']:.4f})"
                similarity_percent = max(0, (1 - row['DISTANCE']) * 100)
                similarity_info = f" • Similarity: {similarity_percent:.1f}%"
            else:
                distance_score = ""
                similarity_info = ""
                
            st.markdown(f"""
            <div class="result-card">
                <div class="movie-title">{row['MOVIE']}<span class="distance-score">{distance_score}</span></div>
                <div class="quote-text">"{row['MOVIE_QUOTE']}"</div>
                <div class="movie-info">{row['MOVIE_TYPE'].title()} • {row['MOVIE_YEAR']}{similarity_info}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Display as table in expander
    with st.expander("View as Data Table"):
        st.dataframe(df, use_container_width=True)

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🎬 Movie Quotes Vector Search</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Database Connection")
        
        # Database connection status
        if st.session_state.connected:
            st.success("✅ Oracle DB Connected (cx_Oracle)")
        else:
            st.error("❌ Database Disconnected")
        
        # Connection button
        if st.button("🔌 Connect to Oracle Database", use_container_width=True):
            connect_to_database()
        
        # Disconnect button
        if st.session_state.connected:
            if st.button("🔌 Disconnect", use_container_width=True):
                if st.session_state.db_connection:
                    st.session_state.db_connection.disconnect()
                st.session_state.connected = False
                st.session_state.db_connection = None
                st.success("Disconnected from database")
        
        st.markdown("---")
        
        # Search settings
        st.header("🎛️ Search Settings")
        search_method = st.selectbox(
            "Search Method",
            ["Vector Search (Oracle AI)", "Text Search (Traditional)"],
            help="Vector search uses Oracle's built-in all_minilm_l12_v2 model for semantic similarity"
        )
        
        if search_method == "Text Search (Traditional)":
            search_scope = st.selectbox(
                "Search In",
                ["Both Movie & Quote", "Movie Title Only", "Quote Only"],
                help="Choose what fields to search in"
            )
        
        top_k = st.slider("Max Results", 5, 50, 10, help="Maximum number of results to return")
        
        st.markdown("---")
        
        # Database info
        if st.session_state.connected:
            st.header("📊 Database Info")
            try:
                # Get total count
                query = "SELECT COUNT(*) as total FROM DEV.MOVIE_QUOTES"
                result = st.session_state.db_connection.execute_query(query)
                if result:
                    total_records = result[0][0]
                    st.metric("Total Movie Quotes", total_records)
                
                # Get movie count by type
                query2 = "SELECT MOVIE_TYPE, COUNT(*) FROM DEV.MOVIE_QUOTES GROUP BY MOVIE_TYPE"
                result2 = st.session_state.db_connection.execute_query(query2)
                if result2:
                    for movie_type, count in result2:
                        st.metric(f"{movie_type.title()}s", count)
                        
            except Exception as e:
                st.error(f"Error fetching database info: {str(e)}")
    
    # Main content
    if not st.session_state.connected:
        st.warning("⚠️ Please connect to the Oracle database first using the sidebar.")
        st.info("Make sure your .env file is properly configured with Oracle database credentials.")
        
        with st.expander("📋 Setup Instructions"):
            st.markdown("""
            **Steps to set up:**
            1. Copy `.env.template` to `.env`
            2. Fill in your Oracle database credentials
            3. Install requirements: `pip install -r requirements.txt`
            4. Click "Connect to Oracle Database" in the sidebar
            
            **Required .env variables:**
            ```
            DB_USER=your_oracle_username
            DB_PASSWORD=your_oracle_password
            DB_HOST=your_oracle_host
            DB_PORT=1521
            DB_SERVICE_NAME=your_service_name
            ```
            """)
        
        # Show some example searches
        st.markdown("### 🎯 Example Vector Searches")
        st.markdown("""
        Try these example searches once connected:
        """)
        
        examples = [
            "Films with motivational speaking in them",
            "Movies about friendship and loyalty", 
            "Action scenes with explosions",
            "Romantic comedy quotes",
            "Villains making threats",
            "Heroic speeches",
            "Funny one-liners"
        ]
        
        cols = st.columns(2)
        for i, example in enumerate(examples):
            with cols[i % 2]:
                st.markdown(f"• *{example}*")
        
        return
    
    # Show random quotes when first connected
    if st.session_state.connected and 'random_quotes_shown' not in st.session_state:
        st.markdown("### 🎲 Featured Movie Quotes")
        vector_utils = VectorSearchUtils()
        random_results, random_columns = vector_utils.get_random_quotes(st.session_state.db_connection, 3)
        if random_results:
            display_results(random_results, random_columns, "text")
        st.session_state.random_quotes_shown = True

    # Search interface
    with st.container():
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            search_query = st.text_input(
                "🔍 Search for movies and quotes:",
                placeholder="Enter your search query (e.g., 'Films with motivational speaking', 'action movie', 'funny quote')",
                help="For vector search: Use natural language. For text search: Use keywords."
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
            search_button = st.button("🚀 Search", use_container_width=True, type="primary")
        
        # Quick search examples
        st.markdown("**Quick Examples:**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🎭 Motivational", help="Films with motivational speaking"):
                st.session_state.quick_search = "Films with motivational speaking in them"
        with col2:
            if st.button("⚔️ Action", help="Action movies"):
                st.session_state.quick_search = "action movie with fighting"
        with col3:
            if st.button("❤️ Romance", help="Romantic quotes"):
                st.session_state.quick_search = "romantic love quotes"
        with col4:
            if st.button("😂 Comedy", help="Funny quotes"):
                st.session_state.quick_search = "funny comedy quotes"
        
        # Handle quick search
        if 'quick_search' in st.session_state:
            search_query = st.session_state.quick_search
            search_button = True
            del st.session_state.quick_search
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Perform search
    if search_button and search_query.strip():
        if not st.session_state.connected:
            st.error("❌ Database connection lost. Please reconnect.")
            return
        
        with st.spinner("Searching Oracle database..."):
            vector_utils = VectorSearchUtils()
            
            if search_method == "Vector Search (Oracle AI)":
                # Vector search using Oracle's native embedding
                results, columns = vector_utils.search_similar_quotes(
                    st.session_state.db_connection, 
                    search_query, 
                    top_k
                )
                if results:
                    st.markdown("### 🎯 Vector Search Results")
                    st.info("Results ranked by semantic similarity using Oracle's all_minilm_l12_v2 model")
                    display_results(results, columns, "vector")
                else:
                    st.warning("No results found. Please check your search query.")
            
            else:
                # Text search
                search_type_map = {
                    "Both Movie & Quote": "both",
                    "Movie Title Only": "movie", 
                    "Quote Only": "quote"
                }
                search_type = search_type_map[search_scope]
                
                results, columns = vector_utils.search_movie_quotes_by_text(
                    st.session_state.db_connection,
                    search_query,
                    search_type
                )
                
                if results:
                    st.markdown("### 📝 Text Search Results")
                    st.info(f"Results from {search_scope.lower()} containing '{search_query}'")
                    display_results(results, columns, "text")
                else:
                    st.warning("No results found matching your search criteria.")
    
    elif search_button and not search_query.strip():
        st.warning("⚠️ Please enter a search query.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d;'>
        <p>🎬 Movie Quotes Vector Search • Powered by Oracle Database 23ai with cx_Oracle</p>
        <p>Vibe coding by VOEURNG SOVANN </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()