## 🔍 Usage Examples

### Vector Search (Semantic)
The application uses Oracle's native `VECTOR_EMBEDDING(all_minilm_l12_v2)` function, equivalent to:

```sql
SELECT vector_distance(movie_quote_vector, 
       (vector_embedding(all_minilm_l12_v2 using 'Films with motivational speaking' as data))) as distance,
       movie,
       movie_quote
FROM   movie_quotes
order by 1
fetch approximate first 5 rows only;
```

**Try these searches:**
- "Films with motivational speaking in them"
- "Movies about friendship and loyalty" 
- "Action scenes with explosions"
- "Romantic comedy quotes"
- "Villains making threats"

### Text Search (Traditional)
- Search by movie title: "Godfather"
- Search by quote content: "may the force"
- Combined search: "star wars"

## 🏗️ Architecture

- **Frontend**: Streamlit web interface
- **Backend**: Oracle Database 23ai with native AI
- **Vector Model**: `all_minilm_l12_v2` (built into Oracle)
- **Search**: `VECTOR_DISTANCE` with cosine similarity
- **Index**: Oracle Vector Index for optimized search# 🎬 Movie Quotes Vector Search Application

A modern Streamlit web application for searching movie quotes using Oracle Database 23ai's native vector search capabilities with the built-in `all_minilm_l12_v2` embedding model.

## 🌟 Features

- **Vector Search**: Semantic search using Oracle's built-in `all_minilm_l12_v2` model and `VECTOR_EMBEDDING` function
- **Text Search**: Traditional keyword-based search in movie titles and quotes
- **Interactive UI**: Clean, responsive Streamlit interface
- **Database Integration**: Oracle Database 23ai with native vector indexing
- **Environment Configuration**: Secure credential management with .env files
- **Virtual Environment**: Isolated Python environment for clean dependencies
- **No External APIs**: Uses Oracle's built-in AI capabilities - no OpenAI API key required!

## 🗃️ Database Schema

The application uses the `DEV.MOVIE_QUOTES` table with the following structure:

- `MOVIE` (VARCHAR2): Movie title
- `MOVIE_QUOTE` (VARCHAR2): Famous quote from the movie
- `MOVIE_TYPE` (VARCHAR2): Type of content (movie/TV show)
- `MOVIE_YEAR` (NUMBER): Release year
- `MOVIE_QUOTE_VECTOR` (VECTOR): Vector embedding for semantic search

**Current Database Stats:**
- **Total Records**: 732 movie quotes
- **Vector Index**: `MOVIE_QUOTES_VECTOR_IDX` for fast similarity search
- **Sample Data**: Quotes from classics like "Gone with the Wind", "The Godfather", "Star Wars"

## 🚀 Quick Start

### 1. Clone and Setup
```bash
# Navigate to your project folder
cd D:\Knowledge\Python\claude\vector_search

# Run the automated setup script
python setup.py
```

### 2. Configure Environment
Edit the `.env` file with your Oracle database credentials:

```env
# Oracle Database Configuration
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=1521
DB_SERVICE_NAME=your_service_name
```

**Note**: No OpenAI API key needed! Oracle Database 23ai handles embeddings natively.

### 3. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 4. Run the Application
```bash
streamlit run app.py
```

### 5. Open in Browser
Navigate to: `http://localhost:8501`

## 📂 Project Structure

```
vector_search/
├── app.py                    # Main Streamlit application
├── database_connection.py    # Oracle database connection handler
├── vector_search_utils.py    # Vector search and embedding utilities
├── requirements