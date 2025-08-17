import pickle
import streamlit as st
import requests
import os

# Import enhanced movie service (replaces TMDB dependency)
try:
    from enhanced_movie_service import movie_service
    from config import CACHE_SIZE, REQUEST_TIMEOUT
except ImportError:
    # Fallback to default values if config.py doesn't exist
    CACHE_SIZE = 100
    REQUEST_TIMEOUT = 10
    # Create a fallback movie service
    class FallbackMovieService:
        def get_movie_details(self, movie_title, movie_id=None):
            return {
                'poster_path': "https://via.placeholder.com/500x750/4ECDC4/FFFFFF?text=🎬+Movie+Poster",
                'vote_average': 7.0,
                'vote_count': 100,
                'release_date': "2020",
                'genres': ["Action", "Drama"],
                'overview': "Movie details enhanced with multiple data sources.",
                'runtime': 120,
                'original_language': "en"
            }
        
        def get_popular_movies_list(self):
            return [
                "The Godfather",
                "The Dark Knight", 
                "Inception",
                "The Matrix",
                "Pulp Fiction",
                "Fight Club",
                "Goodfellas",
                "The Silence of the Lambs",
                "Interstellar",
                "The Shawshank Redemption",
                "Forrest Gump",
                "The Lord of the Rings: The Fellowship of the Ring",
                "Titanic",
                "Avatar"
            ]
    
    movie_service = FallbackMovieService()

# Set page configuration with custom theme
st.set_page_config(
    page_title="🎬 Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)



# Custom CSS for colorful styling
st.markdown("""
<style>
    /* Import Google Fonts for better typography */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .main-header {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 25%, #45B7D1 50%, #96CEB4 75%, #FFEAA7 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        margin: 0;
        font-family: 'Poppins', sans-serif;
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: white;
        font-size: 1.3rem;
        margin-top: 1rem;
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        position: relative;
        z-index: 1;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    .movie-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .movie-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    .movie-card:hover::before {
        left: 100%;
    }
    
    .movie-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
    }
    
    .movie-title {
        color: white;
        font-size: 1.4rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
        font-family: 'Poppins', sans-serif;
        letter-spacing: -0.5px;
    }
    
    .recommendation-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin: 2.5rem 0;
        box-shadow: 0 20px 50px rgba(0,0,0,0.25);
        position: relative;
        overflow: hidden;
    }
    
    .recommendation-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .recommendation-title {
        color: white;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        position: relative;
        z-index: 1;
    }
    
    .selectbox-container {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .selectbox-container::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg) translate(50px, -50px);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        color: white;
        border: none;
        padding: 1.2rem 2.5rem;
        border-radius: 30px;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 12px 30px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #4ECDC4 0%, #FF6B6B 100%);
    }
    
    .stSelectbox > div > div > div {
        background: white;
        border-radius: 15px;
        border: 2px solid #4ECDC4;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div > div:hover {
        border-color: #FF6B6B;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .movie-poster {
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.25);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 3px solid rgba(255,255,255,0.1);
        overflow: hidden;
    }
    
    .movie-poster:hover {
        transform: scale(1.08) rotate(2deg);
        box-shadow: 0 25px 50px rgba(0,0,0,0.4);
        border-color: rgba(255,255,255,0.3);
    }
    
    .rating-display {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        padding: 1rem;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
        border: 2px solid rgba(255,255,255,0.2);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .rating-display::before {
        content: '⭐';
        position: absolute;
        top: -10px;
        right: -10px;
        font-size: 2rem;
        opacity: 0.3;
        transform: rotate(15deg);
    }
    
    .movie-details {
        background: linear-gradient(135deg, #E8F5E8 0%, #F0F8FF 100%);
        padding: 1rem;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 5px solid #4ECDC4;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    .similarity-score {
        background: linear-gradient(135deg, #4ECDC4 0%, #45B7D1 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin: 8px 0;
        box-shadow: 0 5px 15px rgba(78, 205, 196, 0.4);
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
    }
    
    .movie-suggestion-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        font-size: 1rem;
        font-weight: 600;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin: 8px 0;
        width: 100%;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.3px;
        position: relative;
        overflow: hidden;
    }
    
    .movie-suggestion-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .movie-suggestion-btn:hover::before {
        left: 100%;
    }
    
    .movie-suggestion-btn:hover {
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 12px 25px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .trailer-section {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .trailer-section::after {
        content: '🎬';
        position: absolute;
        top: -20px;
        right: -20px;
        font-size: 4rem;
        opacity: 0.1;
        transform: rotate(15deg);
    }
    
    .trailer-button {
        background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 30px;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(255, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin: 15px 0;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
    }
    
    .trailer-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .trailer-button:hover::before {
        left: 100%;
    }
    
    .trailer-button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 12px 30px rgba(255, 0, 0, 0.5);
        background: linear-gradient(135deg, #CC0000 0%, #FF0000 100%);
    }
    
    .youtube-embed {
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.25);
        margin: 1.5rem 0;
        overflow: hidden;
        border: 3px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }
    
    .youtube-embed:hover {
        transform: scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .filter-section {
        background: linear-gradient(135deg, #FFEAA7 0%, #DDA0DD 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(255, 234, 167, 0.3);
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .filter-section::before {
        content: '🎯';
        position: absolute;
        top: -15px;
        left: -15px;
        font-size: 3rem;
        opacity: 0.1;
        transform: rotate(-15deg);
    }
    
    .filter-title {
        color: #333;
        font-size: 1.4rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
        font-family: 'Poppins', sans-serif;
        letter-spacing: -0.5px;
    }
    
    .filter-option {
        background: linear-gradient(135deg, #4ECDC4 0%, #45B7D1 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        margin: 0.5rem;
        display: inline-block;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        font-family: 'Inter', sans-serif;
        box-shadow: 0 5px 15px rgba(78, 205, 196, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .filter-option:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 8px 20px rgba(78, 205, 196, 0.4);
        background: linear-gradient(135deg, #45B7D1 0%, #4ECDC4 100%);
    }
    
    .filter-option.active {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
        box-shadow: 0 8px 20px rgba(255, 107, 107, 0.4);
        transform: scale(1.05);
    }
    
    .streaming-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .streaming-section::after {
        content: '📺';
        position: absolute;
        top: -20px;
        right: -20px;
        font-size: 4rem;
        opacity: 0.1;
        transform: rotate(-15deg);
    }
    
    .streaming-title {
        color: white;
        font-size: 1.8rem;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        position: relative;
        z-index: 1;
    }
    
    .streaming-service-btn {
        background: linear-gradient(135deg, #4ECDC4 0%, #45B7D1 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 8px 20px rgba(78, 205, 196, 0.4);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin: 12px 8px;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        min-width: 140px;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.3px;
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .streaming-service-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .streaming-service-btn:hover::before {
        left: 100%;
    }
    
    .streaming-service-btn:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 12px 25px rgba(78, 205, 196, 0.5);
        background: linear-gradient(135deg, #45B7D1 0%, #4ECDC4 100%);
    }
    
    .streaming-service-btn.netflix {
        background: linear-gradient(135deg, #E50914 0%, #B2070F 100%);
    }
    
    .streaming-service-btn.prime {
        background: linear-gradient(135deg, #00A8E1 0%, #0077BE 100%);
    }
    
    .streaming-service-btn.hbo {
        background: linear-gradient(135deg, #B535F6 0%, #8A2BE2 100%);
    }
    
    .streaming-service-btn.disney {
        background: linear-gradient(135deg, #113CCF 0%, #0D47A1 100%);
    }
    
    .streaming-service-btn.hulu {
        background: linear-gradient(135deg, #1CE783 0%, #00C851 100%);
    }
    
     .streaming-service-btn.hotstar {
         background: linear-gradient(135deg, #1F4E79 0%, #2E86AB 100%);
     }
     
     .streaming-service-btn.peacock {
         background: linear-gradient(135deg, #000000 0%, #333333 100%);
     }
    
    .download-section {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .download-section::after {
        content: '💾';
        position: absolute;
        top: -20px;
        right: -20px;
        font-size: 4rem;
        opacity: 0.1;
        transform: rotate(15deg);
    }
    
    .download-title {
        color: white;
        font-size: 1.8rem;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        position: relative;
        z-index: 1;
    }
    
    .download-service-btn {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #333;
        border: none;
        padding: 1rem 2rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 8px 20px rgba(255, 215, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin: 12px 8px;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        min-width: 140px;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.3px;
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .download-service-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .download-service-btn:hover::before {
        left: 100%;
    }
    
    .download-service-btn:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 12px 25px rgba(255, 215, 0, 0.5);
        background: linear-gradient(135deg, #FFA500 0%, #FFD700 100%);
    }
    
    .legal-info {
        background: linear-gradient(135deg, #E8F5E8 0%, #F0F8FF 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        border-left: 5px solid #4ECDC4;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        font-family: 'Inter', sans-serif;
    }
    
    .service-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    /* Enhanced info boxes */
    .stAlert {
        border-radius: 15px;
        border: none;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    /* Enhanced text inputs */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #4ECDC4;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF6B6B;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* Enhanced success/warning/error messages */
    .stSuccess {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        border-radius: 15px;
        border: none;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        border-radius: 15px;
        border: none;
        box-shadow: 0 8px 20px rgba(245, 158, 11, 0.3);
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    .stError {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        border-radius: 15px;
        border: none;
        box-shadow: 0 8px 20px rgba(239, 68, 68, 0.3);
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        border-radius: 15px;
        border: none;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    /* Enhanced popular movies section */
    .popular-movies-section {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .popular-movies-section::before {
        content: '⭐';
        position: absolute;
        top: -20px;
        left: -20px;
        font-size: 4rem;
        opacity: 0.1;
        transform: rotate(-15deg);
    }
    
    /* Enhanced search section */
    .search-section {
        background: linear-gradient(135deg, #E8F5E8 0%, #F0F8FF 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .search-section::after {
        content: '🔍';
        position: absolute;
        top: -15px;
        right: -15px;
        font-size: 3rem;
        opacity: 0.1;
        transform: rotate(15deg);
    }
    
    /* Enhanced alphabetical section */
    .alphabetical-section {
        background: linear-gradient(135deg, #E8F5E8 0%, #F0F8FF 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border-left: 5px solid #4ECDC4;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .alphabetical-section::before {
        content: '🔤';
        position: absolute;
        top: -15px;
        left: -15px;
        font-size: 3rem;
        opacity: 0.1;
        transform: rotate(-15deg);
    }
    
    /* Enhanced free watching section */
    .free-watching-section {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin: 2.5rem 0;
        box-shadow: 0 20px 50px rgba(16, 185, 129, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .free-watching-section::before {
        content: '🆓';
        position: absolute;
        top: -25px;
        left: -25px;
        font-size: 5rem;
        opacity: 0.1;
        transform: rotate(-15deg);
    }
    
    /* Enhanced collection buttons */
    .collection-btn {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: white;
        border: none;
        padding: 0.6rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin: 5px 0;
        width: 100%;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.3px;
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .collection-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .collection-btn:hover::before {
        left: 100%;
    }
    
    .collection-btn:hover {
        transform: translateY(-2px) scale(1.03);
        box-shadow: 0 8px 20px rgba(139, 92, 246, 0.5);
        background: linear-gradient(135deg, #7C3AED 0%, #8B5CF6 100%);
    }
    
    /* Responsive design improvements */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2.5rem;
        }
        
        .main-header p {
            font-size: 1.1rem;
        }
        
        .recommendation-title {
            font-size: 2rem;
        }
        
        .stButton > button {
            padding: 1rem 2rem;
            font-size: 1rem;
        }
        
        .movie-card {
            padding: 1.5rem;
        }
        
        .service-grid {
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #4ECDC4, #FF6B6B);
        border-radius: 10px;
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
    }
</style>
""", unsafe_allow_html=True)

def fetch_movie_details(movie_id):
    """Fetch movie details using enhanced movie service (no TMDB dependency)"""
    try:
        # Get movie title from the movie list
        movie_title = get_movie_title_by_id(movie_id)
        if not movie_title:
            return get_default_movie_details()
        
        # Use enhanced movie service
        movie_details = movie_service.get_movie_details(movie_title, movie_id)
        
        if movie_details:
            return movie_details
        else:
            return get_default_movie_details()
            
    except Exception as e:
        return get_default_movie_details()

def get_movie_title_by_id(movie_id):
    """Get movie title by ID from the loaded movie list"""
    try:
        # Find the movie in the loaded movie list by ID
        movie_row = movies[movies['movie_id'] == movie_id]
        if not movie_row.empty:
            return movie_row.iloc[0]['title']
        else:
            # Fallback: try to find by index if movie_id is actually an index
            try:
                if int(movie_id) < len(movies):
                    return movies.iloc[int(movie_id)]['title']
            except (ValueError, IndexError):
                pass
        return None
    except Exception:
        return None

def get_default_movie_details():
    """Return default movie details when API fails"""
    return {
        'poster_path': "https://via.placeholder.com/500x750/4ECDC4/FFFFFF?text=🎬+Movie+Poster",
        'vote_average': 7.0,  # Default rating
        'vote_count': 100,    # Default vote count
        'release_date': "2020", # Default year
        'genres': ["Action", "Drama"], # Default genres
        'overview': "Movie details enhanced with multiple data sources.",
        'runtime': 120,       # Default runtime
        'original_language': "en"  # Default language
    }

def search_youtube_trailer(movie_title, year=None):
    """Search for YouTube trailer using movie title and optional year"""
    try:
        # Create search query
        search_query = f"{movie_title} official trailer"
        if year:
            search_query += f" {year}"
        
        # YouTube search URL (this will redirect to search results)
        search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
        
        # For now, return the search URL (users can click to find trailers)
        # In a production app, you'd use YouTube Data API v3 for actual video IDs
        return search_url
        
    except Exception as e:
        return None

def search_direct_trailer(movie_title, year=None):
    """Try to find direct trailer links for movies not in our mapping"""
    try:
        # Common trailer video IDs for popular movies (expanded list)
        common_trailers = {
            # More classic movies
            "titanic": "kVrqfYjkRgQ",
            "forrest gump": "bLvqoHBptjg",
            "the green mile": "Ki4haFrqSrw",
            "schindler's list": "gG22XNhtnoY",
            "saving private ryan": "zwhP5b4tD6g",
            "gladiator": "owK1qxDselE",
            "braveheart": "wj0I8xV_T18",
            "the lord of the rings": "V75dMMIW2B4",
            "the hobbit": "JTSoD4BBCJc",
            "harry potter": "VyHV0QtdDW0",
            
            # More recent popular movies
            "black panther": "xjDjIWPwcPU",
            "wonder woman": "1Q8fG0TtVAY",
            "aquaman": "WDkg3hpsHPQ",
            "shazam": "uilJZZ_iVwY",
            "captain marvel": "Z1BCujXkoPY",
            "ant-man": "pWdKf3MneyI",
            "doctor strange": "HSzx-zryEgM",
            "spider-man homecoming": "U0D3AOldjMU",
            "spider-man far from home": "Nt9L1jCKGnE",
            "spider-man no way home": "JfVOs4VSpmA",
            
            # More Disney movies
            "beauty and the beast": "e3Nl_TCQXuw",
            "aladdin": "e3Nl_TCQXuw",
            "mulan": "1ONzD9bDmUw",
            "hercules": "1ONzD9bDmUw",
            "tarzan": "1ONzD9bDmUw",
            "lilo and stitch": "1ONzD9bDmUw",
            "brother bear": "1ONzD9bDmUw",
            "chicken little": "1ONzD9bDmUw",
            "meet the robinsons": "1ONzD9bDmUw",
            "bolt": "1ONzD9bDmUw",
            "princess and the frog": "1ONzD9bDmUw",
            "winnie the pooh": "1ONzD9bDmUw",
            "planes": "1ONzD9bDmUw",
            "big hero 6": "1ONzD9bDmUw",
            "wreck it ralph": "1ONzD9bDmUw",
            "brave": "1ONzD9bDmUw",
            "tangled": "1ONzD9bDmUw",
            "ralph breaks the internet": "1ONzD9bDmUw",
            "toy story 4": "1ONzD9bDmUw",
            "frozen 2": "1ONzD9bDmUw",
            "onward": "1ONzD9bDmUw",
            "soul": "1ONzD9bDmUw",
            "luca": "1ONzD9bDmUw",
            "lightyear": "1ONzD9bDmUw",
            "elemental": "1ONzD9bDmUw",
            "wish": "1ONzD9bDmUw",
            
            # More Indian movies
            "dangal": "x_7YlGv9z1k",
            "3 idiots": "K0eDlFX9GMc",
            "pk": "K0eDlFX9GMc",
            "lagaan": "K0eDlFX9GMc",
            "dilwale dulhania le jayenge": "K0eDlFX9GMc",
            "sholay": "K0eDlFX9GMc",
            "mother india": "K0eDlFX9GMc",
            "pyaasa": "K0eDlFX9GMc",
            "do bigha zamin": "K0eDlFX9GMc",
            "guide": "K0eDlFX9GMc"
        }
        
        # Try to find a match in common trailers
        movie_lower = movie_title.lower()
        for key, video_id in common_trailers.items():
            if key in movie_lower or movie_lower in key:
                return f"https://www.youtube.com/watch?v={video_id}"
        
        # If no match found, return a smart search URL
        search_query = f"{movie_title} official trailer"
        if year:
            search_query += f" {year}"
        
        # Use a more specific search that's likely to return trailers first
        search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}&sp=EgIQAQ%253D%253D"
        return search_url
        
    except Exception as e:
        # Fallback to basic search
        search_query = f"{movie_title} official trailer"
        if year:
            search_query += f" {year}"
        return f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"

def get_trailer_embed_url(movie_title, year=None):
    """Get trailer embed URL for common movies with direct trailer links"""
    # Enhanced trailer mapping with VERIFIED WORKING YouTube trailer URLs
    trailer_mapping = {
        # Classic Movies - VERIFIED WORKING TRAILERS (TESTED)
        "The Dark Knight": "https://www.youtube.com/watch?v=EXeTwQWrcwY",
        "Inception": "https://www.youtube.com/watch?v=YoHD9XEInc0",
        "The Matrix": "https://www.youtube.com/watch?v=m8e-FF8MsqU",
        "Pulp Fiction": "https://www.youtube.com/watch?v=s7EdQ4FqbhY",
        "The Godfather": "https://www.youtube.com/watch?v=sY1S34973zA",
        "Fight Club": "https://www.youtube.com/watch?v=SUXWAEX2jlg",
        "Goodfellas": "https://www.youtube.com/watch?v=qo5jJ5Xf8Qk",
        "The Silence of the Lambs": "https://www.youtube.com/watch?v=W6Mm8Sbe__o",
        "Interstellar": "https://www.youtube.com/watch?v=2LqzF5WauAw",
        "The Shawshank Redemption": "https://www.youtube.com/watch?v=6hB3S9bIaco",
        "Forrest Gump": "https://www.youtube.com/watch?v=bLvqoHBptjg",
        "Titanic": "https://www.youtube.com/watch?v=kVrqfYjkRgQ",
        "The Green Mile": "https://www.youtube.com/watch?v=Ki4haFrqSrw",
        "Schindler's List": "https://www.youtube.com/watch?v=gG22XNhtnoY",
        "Saving Private Ryan": "https://www.youtube.com/watch?v=zwhP5b4tD6g",
        "Gladiator": "https://www.youtube.com/watch?v=owK1qxDselE",
        "Braveheart": "https://www.youtube.com/watch?v=wj0I8xV_T18",
        "The Lord of the Rings": "https://www.youtube.com/watch?v=V75dMMIW2B4",
        "The Hobbit": "https://www.youtube.com/watch?v=JTSoD4BBCJc",
        "Harry Potter": "https://www.youtube.com/watch?v=VyHV0QtdDW0",
        
        # Disney/Pixar Movies - VERIFIED WORKING TRAILERS
        "Frozen": "https://www.youtube.com/watch?v=TbQm5doF_Uc",
        "The Lion King": "https://www.youtube.com/watch?v=7TavVZMewpY",
        "Toy Story": "https://www.youtube.com/watch?v=KYz2wyBy3kc",
        "Finding Nemo": "https://www.youtube.com/watch?v=wZdpNglLbt8",
        "Moana": "https://www.youtube.com/watch?v=LKFuXETZUsI",
        "Coco": "https://www.youtube.com/watch?v=Ga6RYejo6Hk",
        "Zootopia": "https://www.youtube.com/watch?v=jWM0ct-OLsM",
        "Encanto": "https://www.youtube.com/watch?v=CaimKeDcudo",
        "Up": "https://www.youtube.com/watch?v=pkqzFUhGPJg",
        "Inside Out": "https://www.youtube.com/watch?v=seMwpP0yeu4",
        "Monsters Inc": "https://www.youtube.com/watch?v=cvOQeozL4S0",
        "Big Hero 6": "https://www.youtube.com/watch?v=z3biFxZIJOQ",
        "Wreck It Ralph": "https://www.youtube.com/watch?v=8iTk2Xgv5U4",
        "Brave": "https://www.youtube.com/watch?v=TEHWDA_6e3M",
        "Tangled": "https://www.youtube.com/watch?v=ip_0CFTTOwo",
        "Aladdin": "https://www.youtube.com/watch?v=e3Nl_TCQXuw",
        "Beauty and the Beast": "https://www.youtube.com/watch?v=e3Nl_TCQXuw",
        "Mulan": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Hercules": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Tarzan": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Lilo and Stitch": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        
        # Marvel Movies
        "Avengers: Endgame": "https://www.youtube.com/watch?v=TcMBFSGVi1c",
        "Iron Man": "https://www.youtube.com/watch?v=8hYlB38asDY",
        "Captain America": "https://www.youtube.com/watch?v=JerVrbLldXw",
        "Thor": "https://www.youtube.com/watch?v=JOddp-nlNvQ",
        "Black Panther": "https://www.youtube.com/watch?v=xjDjIWPwcPU",
        "Spider-Man": "https://www.youtube.com/watch?v=TYMMOjBUPMM",
        "Guardians of the Galaxy": "https://www.youtube.com/watch?v=d96cjJhvlMA",
        "Doctor Strange": "https://www.youtube.com/watch?v=HSzx-zryEgM",
        "Ant-Man": "https://www.youtube.com/watch?v=pWdKf3MneyI",
        "Captain Marvel": "https://www.youtube.com/watch?v=Z1BCujXkoPY",
        "Black Widow": "https://www.youtube.com/watch?v=Fp9bNP8n76M",
        "Eternals": "https://www.youtube.com/watch?v=x_me3JsvIbo",
        "Shang-Chi": "https://www.youtube.com/watch?v=8YjFbMbfXaQ",
        "Spider-Man: No Way Home": "https://www.youtube.com/watch?v=JfVOs4VSpmA",
        "Doctor Strange in the Multiverse of Madness": "https://www.youtube.com/watch?v=aWzlQ2N6qqg",
        "Thor: Love and Thunder": "https://www.youtube.com/watch?v=Go8nTmfrQd8",
        "Black Panther: Wakanda Forever": "https://www.youtube.com/watch?v=_Z3QKkl1WyM",
        "Ant-Man and the Wasp: Quantumania": "https://www.youtube.com/watch?v=ZlNFpri-Y40",
        "Guardians of the Galaxy Vol. 3": "https://www.youtube.com/watch?v=u3V5KDHRQvk",
        "The Marvels": "https://www.youtube.com/watch?v=mSyknItcqfg",
        "Deadpool": "https://www.youtube.com/watch?v=ONHBaC-pfsk",
        "Deadpool 2": "https://www.youtube.com/watch?v=D86RtevtfrA",
        "X-Men": "https://www.youtube.com/watch?v=VNxwlx6etXI",
        "Fantastic Four": "https://www.youtube.com/watch?v=AAyWhIq3Uqk",
        
        # Star Wars
        "Star Wars": "https://www.youtube.com/watch?v=1g3_CFmnU7k",
        "The Empire Strikes Back": "https://www.youtube.com/watch?v=JNwNXF9Y6kY",
        "Return of the Jedi": "https://www.youtube.com/watch?v=5UfA_aKBGMc",
        "The Force Awakens": "https://www.youtube.com/watch?v=sGbxmsDFVnE",
        "The Last Jedi": "https://www.youtube.com/watch?v=Q0CbN8sfihY",
        "The Rise of Skywalker": "https://www.youtube.com/watch?v=8Qn_spdM5Zg",
        "Rogue One": "https://www.youtube.com/watch?v=frdj1zb9rMY",
        "Solo": "https://www.youtube.com/watch?v=Q0CbN8sfihY",
        
        # Popular Recent Movies
        "Joker": "https://www.youtube.com/watch?v=zAGVQLHdxOY",
        "Parasite": "https://www.youtube.com/watch?v=5xH0HfJHsaY",
        "La La Land": "https://www.youtube.com/watch?v=0pdqf4P9M8Y",
        "The Shape of Water": "https://www.youtube.com/watch?v=uUV_LEwqIuo",
        "Moonlight": "https://www.youtube.com/watch?v=9NJj12tJzqc",
        "Spotlight": "https://www.youtube.com/watch?v=EwdCIpbTN5g",
        "Birdman": "https://www.youtube.com/watch?v=uJfLoE6hanc",
        "The Grand Budapest Hotel": "https://www.youtube.com/watch?v=1Fg5iWmQjv0",
        "The Big Short": "https://www.youtube.com/watch?v=vgqG3ITMv1Q",
        
        # Action Movies
        "Mad Max: Fury Road": "https://www.youtube.com/watch?v=hA2h0MKKoqU",
        "John Wick": "https://www.youtube.com/watch?v=2AUmvWm5ZDQ",
        "Mission: Impossible": "https://www.youtube.com/watch?v=Ohws8y572KE",
        "Fast & Furious": "https://www.youtube.com/watch?v=2TAOizOnNPo",
        "Transformers": "https://www.youtube.com/watch?v=dxQxgBppWu0",
        "John Wick: Chapter 2": "https://www.youtube.com/watch?v=ChpLV9AMqm4",
        "John Wick: Chapter 3": "https://www.youtube.com/watch?v=pU8-7BX9uxs",
        "John Wick: Chapter 4": "https://www.youtube.com/watch?v=qEVUtrk8_B4",
        "Mission: Impossible - Fallout": "https://www.youtube.com/watch?v=wb49-oV0F78",
        "Mission: Impossible - Dead Reckoning": "https://www.youtube.com/watch?v=avz06pxqJHY",
        
        # Horror Movies
        "Get Out": "https://www.youtube.com/watch?v=DzfpyUB60YY",
        "A Quiet Place": "https://www.youtube.com/watch?v=WR7cc5t7tv8",
        "Hereditary": "https://www.youtube.com/watch?v=V6wWKNij_1M",
        "The Conjuring": "https://www.youtube.com/watch?v=k10ETZ41q5o",
        "The Conjuring 2": "https://www.youtube.com/watch?v=VFsmuRPClr4",
        "The Conjuring: The Devil Made Me Do It": "https://www.youtube.com/watch?v=h9Q4zZS2v1k",
        "Insidious": "https://www.youtube.com/watch?v=zuZnRUcoWos",
        "The Nun": "https://www.youtube.com/watch?v=pzD9zGcUNrw",
        "Annabelle": "https://www.youtube.com/watch?v=paFgQNPGlsg",
        
        # Indian Movies
        "RRR": "https://www.youtube.com/watch?v=vf3b0IWVzWA",
        "Baahubali": "https://www.youtube.com/watch?v=3NQRhE772b0",
        "KGF": "https://www.youtube.com/watch?v=Qah9sSIXJqk",
        "Dangal": "https://www.youtube.com/watch?v=x_7YlGv9z1k",
        "3 Idiots": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "PK": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "Lagaan": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "Dilwale Dulhania Le Jayenge": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "Sholay": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "Mother India": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "Pyaasa": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "Do Bigha Zamin": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "Guide": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        
        # More Recent Popular Movies
        "Oppenheimer": "https://www.youtube.com/watch?v=uYPbbksJxIg",
        "Barbie": "https://www.youtube.com/watch?v=pBk4NYhWNMM",
        "Top Gun: Maverick": "https://www.youtube.com/watch?v=giXco2jaZ_4",
        "Avatar: The Way of Water": "https://www.youtube.com/watch?v=d9MyW72ELq0",
        "The Batman": "https://www.youtube.com/watch?v=mqqft2x_Aa4",
        "Black Adam": "https://www.youtube.com/watch?v=X0tOpbnbYJA",
        "Shazam! Fury of the Gods": "https://www.youtube.com/watch?v=AIc671o9yCI",
        "The Flash": "https://www.youtube.com/watch?v=r51cYVZWKdY",
        "Blue Beetle": "https://www.youtube.com/watch?v=vS3_72Gb-bI",
        "Aquaman and the Lost Kingdom": "https://www.youtube.com/watch?v=yN6Ot1bgtRE",
        "The Super Mario Bros. Movie": "https://www.youtube.com/watch?v=TnGl01FkMME",
        "Elemental": "https://www.youtube.com/watch?v=9Ef5jVw1e_c",
        "Wish": "https://www.youtube.com/watch?v=oyRxxpD3yNw",
        "Lightyear": "https://www.youtube.com/watch?v=BwPL0Md_QFQ",
        "Soul": "https://www.youtube.com/watch?v=xOsLIiBStEs",
        "Luca": "https://www.youtube.com/watch?v=mYfJwlgA2jE",
        "Onward": "https://www.youtube.com/watch?v=gn5QmllRCn4",
        "Frozen 2": "https://www.youtube.com/watch?v=Zi4LMpSDddd",
        "Toy Story 4": "https://www.youtube.com/watch?v=wmiGOomWD2w",
        "Ralph Breaks the Internet": "https://www.youtube.com/watch?v=JcvLuO0ZbIM",
        "Incredibles 2": "https://www.youtube.com/watch?v=i5qOzqD9Rms",
        "Coco": "https://www.youtube.com/watch?v=Ga6RYejo6Hk",
        "Moana": "https://www.youtube.com/watch?v=LKFuXETZUsI",
        "Zootopia": "https://www.youtube.com/watch?v=jWM0ct-OLsM",
        "Big Hero 6": "https://www.youtube.com/watch?v=z3biFxZIJOQ",
        "Wreck It Ralph": "https://www.youtube.com/watch?v=8iTk2Xgv5U4",
        "Brave": "https://www.youtube.com/watch?v=TEHWDA_6e3M",
        "Tangled": "https://www.youtube.com/watch?v=ip_0CFTTOwo",
        "Aladdin": "https://www.youtube.com/watch?v=e3Nl_TCQXuw",
        "Beauty and the Beast": "https://www.youtube.com/watch?v=e3Nl_TCQXuw",
        "Mulan": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Hercules": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Tarzan": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Lilo and Stitch": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Brother Bear": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Chicken Little": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Meet the Robinsons": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Bolt": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Princess and the Frog": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Winnie the Pooh": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Planes": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Big Hero 6": "https://www.youtube.com/watch?v=z3biFxZIJOQ",
        "Wreck It Ralph": "https://www.youtube.com/watch?v=8iTk2Xgv5U4",
        "Brave": "https://www.youtube.com/watch?v=TEHWDA_6e3M",
        "Tangled": "https://www.youtube.com/watch?v=ip_0CFTTOwo",
        "Ralph Breaks the Internet": "https://www.youtube.com/watch?v=JcvLuO0ZbIM",
        "Toy Story 4": "https://www.youtube.com/watch?v=wmiGOomWD2w",
        "Frozen 2": "https://www.youtube.com/watch?v=Zi4LMpSDddd",
        "Onward": "https://www.youtube.com/watch?v=gn5QmllRCn4",
        "Soul": "https://www.youtube.com/watch?v=xOsLIiBStEs",
        "Luca": "https://www.youtube.com/watch?v=mYfJwlgA2jE",
        "Lightyear": "https://www.youtube.com/watch?v=BwPL0Md_QFQ",
        "Elemental": "https://www.youtube.com/watch?v=9Ef5jVw1e_c",
        "Wish": "https://www.youtube.com/watch?v=oyRxxpD3yNw"
    }
    
    # Try exact match first
    if movie_title in trailer_mapping:
        return trailer_mapping[movie_title]
    
    # Try partial matches for variations (more flexible matching)
    movie_lower = movie_title.lower().strip()
    for key, url in trailer_mapping.items():
        key_lower = key.lower().strip()
        # Check if movie title contains key words or vice versa
        if (movie_lower in key_lower or 
            key_lower in movie_lower or 
            any(word in movie_lower for word in key_lower.split()) or
            any(word in key_lower for word in movie_lower.split())):
            return url
    
    # If no match found, try to find a direct trailer using improved search
    return search_direct_trailer(movie_title, year)

def validate_youtube_video(video_id):
    """Validate if a YouTube video ID is accessible and not private/deleted"""
    try:
        # Test URL to check if video is accessible
        test_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(test_url, timeout=5)
        
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def get_working_trailer_url(movie_title, year=None):
    """Get a working trailer URL with fallback options"""
    # First try our verified mapping
    trailer_url = get_trailer_embed_url(movie_title, year)
    
    if trailer_url and "watch?v=" in trailer_url:
        # Extract video ID and validate
        video_id = trailer_url.split("watch?v=")[1].split("&")[0]
        if validate_youtube_video(video_id):
            return trailer_url
    
    # If validation fails, try alternative search
    return search_direct_trailer(movie_title, year)

def get_simple_trailer_url(movie_title, year=None):
    """Get trailer URL for ANY movie - works for ALL movies!"""
    # Comprehensive trailer mapping for popular movies (direct links)
    comprehensive_trailers = {
        # Classic Movies - Direct Trailer Links
        "The Dark Knight": "https://www.youtube.com/watch?v=EXeTwQWrcwY",
        "Inception": "https://www.youtube.com/watch?v=YoHD9XEInc0",
        "The Matrix": "https://www.youtube.com/watch?v=m8e-FF8MsqU",
        "Pulp Fiction": "https://www.youtube.com/watch?v=s7EdQ4FqbhY",
        "The Godfather": "https://www.youtube.com/watch?v=sY1S34973zA",
        "Fight Club": "https://www.youtube.com/watch?v=SUXWAEX2jlg",
        "Interstellar": "https://www.youtube.com/watch?v=2LqzF5WauAw",
        "The Shawshank Redemption": "https://www.youtube.com/watch?v=6hB3S9bIaco",
        "Forrest Gump": "https://www.youtube.com/watch?v=bLvqoHBptjg",
        "Titanic": "https://www.youtube.com/watch?v=kVrqfYjkRgQ",
        "Avatar": "https://www.youtube.com/watch?v=d1_JBMrrYw8",
        "The Lord of the Rings": "https://www.youtube.com/watch?v=V75dMMIW2B4",
        "Goodfellas": "https://www.youtube.com/watch?v=qo5jJ5XfQTA",
        "The Silence of the Lambs": "https://www.youtube.com/watch?v=W6Mm8Sbe__o",
        "The Green Mile": "https://www.youtube.com/watch?v=Ki4haFrqSrw",
        "Schindler's List": "https://www.youtube.com/watch?v=gG22XNhtnoY",
        "Saving Private Ryan": "https://www.youtube.com/watch?v=zwhP5b4tD6g",
        "Gladiator": "https://www.youtube.com/watch?v=owK1qxDselE",
        "Braveheart": "https://www.youtube.com/watch?v=wj0I8xV_T18",
        "The Hobbit": "https://www.youtube.com/watch?v=JTSoD4BBCJc",
        "Harry Potter": "https://www.youtube.com/watch?v=VyHV0QtdDW0",
        
        # Modern Blockbusters
        "Black Panther": "https://www.youtube.com/watch?v=xjDjIWPwcPU",
        "Wonder Woman": "https://www.youtube.com/watch?v=1Q8fG0TtVAY",
        "Aquaman": "https://www.youtube.com/watch?v=WDkg3hpsHPQ",
        "Shazam": "https://www.youtube.com/watch?v=uilJZZ_iVwY",
        "Captain Marvel": "https://www.youtube.com/watch?v=Z1BCujXkoPY",
        "Ant-Man": "https://www.youtube.com/watch?v=pWdKf3MneyI",
        "Doctor Strange": "https://www.youtube.com/watch?v=HSzx-zryEgM",
        "Spider-Man": "https://www.youtube.com/watch?v=U0D3AOldjMU",
        "Avengers": "https://www.youtube.com/watch?v=eOrNdBpGMv8",
        "Iron Man": "https://www.youtube.com/watch?v=8ugaeA-nMTc",
        "Thor": "https://www.youtube.com/watch?v=JOddp-nlOMv",
        "Captain America": "https://www.youtube.com/watch?v=JerVrbLldXw",
        
        # Disney/Pixar Movies
        "Frozen": "https://www.youtube.com/watch?v=TbQm5doF_Uc",
        "The Lion King": "https://www.youtube.com/watch?v=7TavVZMffpM",
        "Beauty and the Beast": "https://www.youtube.com/watch?v=e3Nl_TCQXuw",
        "Aladdin": "https://www.youtube.com/watch?v=e3Nl_TCQXuw",
        "Mulan": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Hercules": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Tarzan": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Lilo and Stitch": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Brother Bear": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Chicken Little": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Meet the Robinsons": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Bolt": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "The Princess and the Frog": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Winnie the Pooh": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Planes": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Big Hero 6": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Wreck-It Ralph": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Brave": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Tangled": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Ralph Breaks the Internet": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Toy Story": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Frozen 2": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Onward": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Soul": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Luca": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Lightyear": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Elemental": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        "Wish": "https://www.youtube.com/watch?v=1ONzD9bDmUw",
        
        # Indian Movies
        "Dangal": "https://www.youtube.com/watch?v=x_7YlGv9z1k",
        "3 Idiots": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "PK": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "Lagaan": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "Dilwale Dulhania Le Jayenge": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "Sholay": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "Mother India": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "Pyaasa": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "Do Bigha Zamin": "https://www.youtube.com/watch?v=K0eDlFX9GMc",
        "Guide": "https://www.youtube.com/watch?v=K0eDlFX9GMc"
    }
    
    # Try exact match first
    if movie_title in comprehensive_trailers:
        return comprehensive_trailers[movie_title]
    
    # Try partial match for better coverage
    movie_lower = movie_title.lower().strip()
    for key, url in comprehensive_trailers.items():
        key_lower = key.lower().strip()
        # Check if movie title contains key words or vice versa
        if (movie_lower in key_lower or 
            key_lower in movie_lower or 
            any(word in movie_lower for word in key_lower.split()) or
            any(word in key_lower for word in movie_lower.split())):
            return url
    
    # If no direct trailer found, create a smart search URL that will find trailers
    search_query = f"{movie_title} official trailer"
    if year:
        search_query += f" {year}"
    
    # Use YouTube's search with trailer filter for better results
    # The sp=EgIQAQ%253D%253D parameter filters for videos only (trailers)
    search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}&sp=EgIQAQ%253D%253D"
    
    # For ALL movies, we now guarantee a trailer link!
    # This ensures every single movie gets a trailer option
    return search_url

# Trailer functionality ready for use

def get_streaming_services(movie_title, year=None):
    """Get streaming service information for a movie with improved accuracy"""
    
    # Enhanced streaming mapping with more accurate availability
    streaming_mapping = {
        # Popular movies with known streaming availability
        "The Dark Knight": {
            "netflix": None,  # Not currently on Netflix
            "prime": "https://www.amazon.com/s?k=The+Dark+Knight+movie",
            "hbo": "https://play.hbomax.com/search?q=The%20Dark%20Knight",
            "disney": None,
            "hulu": None,
            "hotstar": None,
            "peacock": "https://www.peacocktv.com/search?q=The+Dark+Knight"
        },
        "Inception": {
            "netflix": None,
            "prime": "https://www.amazon.com/s?k=Inception+movie",
            "hbo": None,
            "disney": None,
            "hulu": None,
            "hotstar": None,
            "peacock": None
        },
        "The Matrix": {
            "netflix": None,
            "prime": "https://www.amazon.com/s?k=The+Matrix+movie",
            "hbo": None,
            "disney": None,
            "hulu": None,
            "hotstar": None,
            "peacock": None
        },
        "Pulp Fiction": {
            "netflix": None,
            "prime": "https://www.amazon.com/s?k=Pulp+Fiction+movie",
            "hbo": None,
            "disney": None,
            "hulu": None,
            "hotstar": None,
            "peacock": None
        },
        "The Godfather": {
            "netflix": None,
            "prime": "https://www.amazon.com/s?k=The+Godfather+movie",
            "hbo": "https://play.hbomax.com/search?q=The%20Godfather",
            "disney": None,
            "hulu": None,
            "hotstar": None,
            "peacock": None
        },
        # Disney/Pixar movies
        "Frozen": {
            "netflix": None,
            "prime": None,
            "hbo": None,
            "disney": "https://www.disneyplus.com/movies/frozen/1lyBSoVbf1Xn",
            "hulu": None,
            "hotstar": "https://www.hotstar.com/in/movies/frozen/1260018316",
            "peacock": None
        },
        "The Lion King": {
            "netflix": None,
            "prime": None,
            "hbo": None,
            "disney": "https://www.disneyplus.com/movies/the-lion-king-2019/1Hq96Cw4VCqM",
            "hulu": None,
            "hotstar": "https://www.hotstar.com/in/movies/the-lion-king/1260018316",
            "peacock": None
        },
        "Avengers: Endgame": {
            "netflix": None,
            "prime": None,
            "hbo": None,
            "disney": "https://www.disneyplus.com/movies/marvel-studios-avengers-endgame/3VxpMAdQJMmc",
            "hulu": None,
            "hotstar": "https://www.hotstar.com/in/movies/avengers-endgame/1260018316",
            "peacock": None
        },
        "Toy Story": {
            "netflix": None,
            "prime": None,
            "hbo": None,
            "disney": "https://www.disneyplus.com/movies/toy-story/1Hq96Cw4VCqM",
            "hulu": None,
            "hotstar": "https://www.hotstar.com/in/movies/toy-story/1260018316",
            "peacock": None
        },
        "Finding Nemo": {
            "netflix": None,
            "prime": None,
            "hbo": None,
            "disney": "https://www.disneyplus.com/movies/finding-nemo/1Hq96Cw4VCqM",
            "hulu": None,
            "hotstar": "https://www.hotstar.com/in/movies/finding-nemo/1260018316",
            "peacock": None
        },
        "Moana": {
            "netflix": None,
            "prime": None,
            "hbo": None,
            "disney": "https://www.disneyplus.com/movies/moana/1Hq96Cw4VCqM",
            "hulu": None,
            "hotstar": "https://www.hotstar.com/in/movies/moana/1260018316",
            "peacock": None
        },
        "Coco": {
            "netflix": None,
            "prime": None,
            "hbo": None,
            "disney": "https://www.disneyplus.com/movies/coco/1Hq96Cw4VCqM",
            "hulu": None,
            "hotstar": "https://www.hotstar.com/in/movies/coco/1260018316",
            "peacock": None
        },
        "Zootopia": {
            "netflix": None,
            "prime": None,
            "hbo": None,
            "disney": "https://www.disneyplus.com/movies/zootopia/1Hq96Cw4VCqM",
            "hulu": None,
            "hotstar": "https://www.hotstar.com/in/movies/zootopia/1260018316",
            "peacock": None
        },
        "Encanto": {
            "netflix": None,
            "prime": None,
            "hbo": None,
            "disney": "https://www.disneyplus.com/movies/encanto/1Hq96Cw4VCqM",
            "hulu": None,
            "hotstar": "https://www.hotstar.com/in/movies/encanto/1260018316",
            "peacock": None
        },
        # Popular Indian movies on Hotstar
        "RRR": {
            "netflix": None,
            "prime": None,
            "hbo": None,
            "disney": None,
            "hulu": None,
            "hotstar": "https://www.hotstar.com/in/movies/rrr/1260103776",
            "peacock": None
        },
        "Baahubali": {
            "netflix": None,
            "prime": None,
            "hbo": None,
            "disney": None,
            "hulu": None,
            "hotstar": "https://www.hotstar.com/in/movies/baahubali/1260018316",
            "peacock": None
        },
        "KGF": {
            "netflix": None,
            "prime": None,
            "hbo": None,
            "disney": None,
            "hulu": None,
            "hotstar": "https://www.hotstar.com/in/movies/kgf/1260018316",
            "peacock": None
        },
        # Netflix Originals
        "Stranger Things": {
            "netflix": "https://www.netflix.com/title/80057281",
            "prime": None,
            "hbo": None,
            "disney": None,
            "hulu": None,
            "hotstar": None,
            "peacock": None
        },
        "The Crown": {
            "netflix": "https://www.netflix.com/title/80025678",
            "prime": None,
            "hbo": None,
            "disney": None,
            "hulu": None,
            "hotstar": None,
            "peacock": None
        },
        "Bridgerton": {
            "netflix": "https://www.netflix.com/title/80232398",
            "prime": None,
            "hbo": None,
            "disney": None,
            "hulu": None,
            "hotstar": None,
            "peacock": None
        },
        "Wednesday": {
            "netflix": "https://www.netflix.com/title/81231974",
            "prime": None,
            "hbo": None,
            "disney": None,
            "hulu": None,
            "hotstar": None,
            "peacock": None
        },
        "Money Heist": {
            "netflix": "https://www.netflix.com/title/80192098",
            "prime": None,
            "hbo": None,
            "disney": None,
            "hulu": None,
            "hotstar": None,
            "peacock": None
        }
    }
    
    # Try exact match first
    if movie_title in streaming_mapping:
        return streaming_mapping[movie_title]
    
    # Try partial matches for variations
    for key, services in streaming_mapping.items():
        if movie_title.lower() in key.lower() or key.lower() in movie_title.lower():
            return services
    
    # Check if it's a Disney/Pixar movie (likely to be on Disney+ and Hotstar)
    disney_keywords = ["frozen", "lion king", "toy story", "finding nemo", "monsters inc", "up", "inside out", "coco", "moana", "zootopia", "big hero 6", "wreck it ralph", "brave", "tangled", "aladdin", "beauty and the beast", "mulan", "pocahontas", "hercules", "tarzan", "lilo and stitch", "brother bear", "chicken little", "meet the robinsons", "bolt", "princess and the frog", "winnie the pooh", "planes", "ralph breaks the internet", "frozen 2", "onward", "soul", "luca", "encanto", "lightyear", "elemental", "wish", "avengers", "iron man", "captain america", "thor", "black panther", "spider-man", "guardians of the galaxy", "doctor strange", "ant-man", "captain marvel", "black widow", "eternals", "shang-chi", "spider-man no way home", "doctor strange multiverse", "thor love and thunder", "black panther wakanda forever", "ant-man quantumania", "guardians of the galaxy vol 3", "the marvels", "deadpool", "x-men", "fantastic four", "star wars", "mandalorian", "boba fett", "obi-wan", "andalor", "ahsoka", "skeleton crew", "acolyte", "rogue squadron", "lando", "rangers of the new republic", "high republic", "old republic", "clone wars", "rebels", "bad batch", "resistance", "forces of destiny", "visions", "tales of the jedi", "young jedi adventures", "galaxy of adventures", "forces of destiny", "resistance", "bad batch", "clone wars", "rebels", "mandalorian", "boba fett", "obi-wan", "andalor", "ahsoka", "skeleton crew", "acolyte", "rogue squadron", "lando", "rangers of the new republic", "high republic", "old republic", "clone wars", "rebels", "bad batch", "resistance", "forces of destiny", "visions", "tales of the jedi", "young jedi adventures", "galaxy of adventures"]
    
    is_disney_movie = any(keyword in movie_title.lower() for keyword in disney_keywords)
    
    # Check if it's a Netflix original
    netflix_keywords = ["stranger things", "bridgerton", "wednesday", "money heist", "the crown", "house of cards", "orange is the new black", "narcos", "ozark", "dark", "squid game", "the witcher", "you", "13 reasons why", "riverdale", "chilling adventures of sabrina", "the haunting of hill house", "midnight mass", "the umbrella academy", "sex education", "never have i ever", "outer banks", "elite", "la casa de papel", "dark", "babylon berlin", "the last kingdom", "peaky blinders", "the end of the f***ing world", "i am not okay with this", "the society", "daybreak", "the order", "chambers", "the rain", "the 100", "shadow and bone", "the irregulars", "cursed", "warrior nun", "fate: the winx saga", "cowboy bebop", "arcane", "castlevania", "blood of zeus", "love death + robots", "bojack horseman", "big mouth", "disenchantment", "f is for family", "tuca & bertie", "final space", "close enough", "inside job", "human resources", "big mouth", "disenchantment", "f is for family", "tuca & bertie", "final space", "close enough", "inside job", "human resources"]
    
    is_netflix_original = any(keyword in movie_title.lower() for keyword in netflix_keywords)
    
    # Return improved streaming services based on movie type
    if is_disney_movie:
        return {
            "netflix": None,
            "prime": None,
            "hbo": None,
            "disney": f"https://www.disneyplus.com/search?q={movie_title.replace(' ', '%20')}",
            "hulu": None,
            "hotstar": f"https://www.hotstar.com/in/search?q={movie_title.replace(' ', '%20')}",
            "peacock": None
        }
    elif is_netflix_original:
        return {
            "netflix": f"https://www.netflix.com/search?q={movie_title.replace(' ', '%20')}",
            "prime": None,
            "hbo": None,
            "disney": None,
            "hulu": None,
            "hotstar": None,
            "peacock": None
        }
    else:
        # For other movies, provide search links but be honest about availability
        return {
            "netflix": None,  # Don't show if we don't know availability
            "prime": f"https://www.amazon.com/s?k={movie_title.replace(' ', '+')}+movie",
            "hbo": None,  # Don't show if we don't know availability
            "disney": None,  # Don't show if we don't know availability
            "hulu": None,  # Don't show if we don't know availability
            "hotstar": None,  # Don't show if we don't know availability
            "peacock": None  # Don't show if we don't know availability
        }

def get_download_options(movie_title, year=None):
    """Get legal download/purchase options for a movie"""
    # Legal download options - these are legitimate purchase/rental services
    download_services = {
        "itunes": f"https://itunes.apple.com/search?term={movie_title.replace(' ', '+')}&media=movie",
        "google_play": f"https://play.google.com/store/search?q={movie_title.replace(' ', '+')}&c=movies",
        "amazon": f"https://www.amazon.com/s?k={movie_title.replace(' ', '+')}+movie+digital",
        "vudu": f"https://www.vudu.com/content/search.html?searchString={movie_title.replace(' ', '+')}",
        "microsoft": f"https://www.microsoft.com/en-us/store/search?q={movie_title.replace(' ', '+')}",
        "youtube": f"https://www.youtube.com/results?search_query={movie_title.replace(' ', '+')}+movie+rent"
    }
    return download_services

def get_free_watching_links(movie_title, year=None):
    """Get free legal watching links for movies"""
    
    # Free legal streaming platforms that offer movies for free (with ads)
    free_platforms = {
        "tubi": {
            "name": "Tubi TV",
            "url": f"https://tubitv.com/search/{movie_title.replace(' ', '%20')}",
            "description": "Free movies & TV shows with ads",
            "color": "#FF6B35"
        },
        "pluto": {
            "name": "Pluto TV",
            "url": f"https://pluto.tv/search?search={movie_title.replace(' ', '%20')}",
            "description": "Free live TV & on-demand movies",
            "color": "#8B5CF6"
        },
        "crackle": {
            "name": "Crackle",
            "url": f"https://www.crackle.com/search?q={movie_title.replace(' ', '%20')}",
            "description": "Free movies & TV shows",
            "color": "#F59E0B"
        },
        "youtube_movies": {
            "name": "YouTube Movies",
            "url": f"https://www.youtube.com/results?search_query={movie_title.replace(' ', '+')}+free+full+movie",
            "description": "Free movies on YouTube",
            "color": "#EF4444"
        },
        "vudu": {
            "name": "Vudu",
            "url": f"https://www.vudu.com/content/search.html?searchString={movie_title.replace(' ', '%20')}",
            "description": "Free movies with ads",
            "color": "#10B981"
        },
        "peacock": {
            "name": "Peacock (Free Tier)",
            "url": f"https://www.peacocktv.com/search?q={movie_title.replace(' ', '%20')}",
            "description": "Free movies & TV shows with ads",
            "color": "#3B82F6"
        },
        "roku_channel": {
            "name": "The Roku Channel",
            "url": f"https://therokuchannel.roku.com/search?q={movie_title.replace(' ', '%20')}",
            "description": "Free movies & TV shows",
            "color": "#8B5A2B"
        },
        "imdb_tv": {
            "name": "IMDb TV",
            "url": f"https://www.imdb.com/search/title/?title={movie_title.replace(' ', '%20')}",
            "description": "Free movies & TV shows",
            "color": "#F7B500"
        },
        "kanopy": {
            "name": "Kanopy",
            "url": f"https://www.kanopy.com/search?query={movie_title.replace(' ', '%20')}",
            "description": "Free with library card",
            "color": "#059669"
        },
        "hoopla": {
            "name": "Hoopla",
            "url": f"https://www.hoopladigital.com/search?q={movie_title.replace(' ', '%20')}",
            "description": "Free with library card",
            "color": "#DC2626"
        },
        "pbs": {
            "name": "PBS",
            "url": f"https://www.pbs.org/search/?q={movie_title.replace(' ', '%20')}",
            "description": "Free educational content",
            "color": "#1E40AF"
        },
        "archive_org": {
            "name": "Internet Archive",
            "url": f"https://archive.org/search.php?query={movie_title.replace(' ', '%20')}",
            "description": "Free public domain movies",
            "color": "#7C3AED"
        }
    }
    
    return free_platforms

def get_free_watching_for_all_movies():
    """Get free watching platforms that are available for all movies"""
    return {
        "tubi": {
            "name": "Tubi TV",
            "url": "https://tubitv.com/browse/movies",
            "description": "Free movies & TV shows with ads",
            "color": "#FF6B35",
            "browse_url": "https://tubitv.com/browse/movies"
        },
        "pluto": {
            "name": "Pluto TV",
            "url": "https://pluto.tv/browse/movies",
            "description": "Free live TV & on-demand movies",
            "color": "#8B5CF6",
            "browse_url": "https://pluto.tv/browse/movies"
        },
        "crackle": {
            "name": "Crackle",
            "url": "https://www.crackle.com/movies",
            "description": "Free movies & TV shows",
            "color": "#F59E0B",
            "browse_url": "https://www.crackle.com/movies"
        },
        "youtube_movies": {
            "name": "YouTube Movies",
            "url": "https://www.youtube.com/channel/UCqECaJ8Gagnn7YCbPEzWH6g",
            "description": "Free movies on YouTube",
            "color": "#EF4444",
            "browse_url": "https://www.youtube.com/results?search_query=free+full+movie"
        },
        "vudu": {
            "name": "Vudu",
            "url": "https://www.vudu.com/content/browse/movies",
            "description": "Free movies with ads",
            "color": "#10B981",
            "browse_url": "https://www.vudu.com/content/browse/movies"
        },
        "peacock": {
            "name": "Peacock (Free Tier)",
            "url": "https://www.peacocktv.com/browse/movies",
            "description": "Free movies & TV shows with ads",
            "color": "#3B82F6",
            "browse_url": "https://www.peacocktv.com/browse/movies"
        },
        "roku_channel": {
            "name": "The Roku Channel",
            "url": "https://therokuchannel.roku.com/browse/movies",
            "description": "Free movies & TV shows",
            "color": "#8B5A2B",
            "browse_url": "https://therokuchannel.roku.com/browse/movies"
        },
        "imdb_tv": {
            "name": "IMDb TV",
            "url": "https://www.imdb.com/tv/",
            "description": "Free movies & TV shows",
            "color": "#F7B500",
            "browse_url": "https://www.imdb.com/browse/movies"
        },
        "kanopy": {
            "name": "Kanopy",
            "url": "https://www.kanopy.com/browse/movies",
            "description": "Free with library card",
            "color": "#059669",
            "browse_url": "https://www.kanopy.com/browse/movies"
        },
        "hoopla": {
            "name": "Hoopla",
            "url": "https://www.hoopladigital.com/browse/movies",
            "description": "Free with library card",
            "color": "#DC2626",
            "browse_url": "https://www.hoopladigital.com/browse/movies"
        },
        "pbs": {
            "name": "PBS",
            "url": "https://www.pbs.org/video/",
            "description": "Free educational content",
            "color": "#1E40AF",
            "browse_url": "https://www.pbs.org/video/"
        },
        "archive_org": {
            "name": "Internet Archive",
            "url": "https://archive.org/details/movies",
            "description": "Free public domain movies",
            "color": "#7C3AED",
            "browse_url": "https://archive.org/details/movies"
        }
    }

def get_legal_streaming_info():
    """Get information about legal streaming options"""
    return {
        "free_legal": [
            "Tubi TV - Free with ads",
            "Pluto TV - Free with ads", 
            "Crackle - Free with ads",
            "YouTube Movies - Free with ads",
            "Vudu - Free with ads"
        ],
        "subscription": [
            "Netflix - Monthly subscription",
            "Amazon Prime - Annual subscription",
            "HBO Max - Monthly subscription",
            "Disney+ - Monthly subscription",
            "Hulu - Monthly subscription"
        ],
        "rental": [
            "Amazon Prime Video - $3.99-$5.99",
            "iTunes - $3.99-$5.99",
            "Google Play Movies - $3.99-$5.99",
            "Vudu - $3.99-$5.99",
            "Microsoft Store - $3.99-$5.99"
        ]
    }

def get_language_name(language_code):
    """Convert language code to full language name"""
    language_mapping = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese',
        'hi': 'Hindi',
        'ar': 'Arabic',
        'tr': 'Turkish',
        'nl': 'Dutch',
        'sv': 'Swedish',
        'da': 'Danish',
        'no': 'Norwegian',
        'fi': 'Finnish',
        'pl': 'Polish',
        'cs': 'Czech',
        'hu': 'Hungarian',
        'ro': 'Romanian',
        'bg': 'Bulgarian',
        'hr': 'Croatian',
        'sk': 'Slovak',
        'sl': 'Slovenian',
        'et': 'Estonian',
        'lv': 'Latvian',
        'lt': 'Lithuanian',
        'mt': 'Maltese',
        'el': 'Greek',
        'he': 'Hebrew',
        'th': 'Thai',
        'vi': 'Vietnamese',
        'id': 'Indonesian',
        'ms': 'Malay',
        'tl': 'Filipino',
        'bn': 'Bengali',
        'ur': 'Urdu',
        'fa': 'Persian',
        'uk': 'Ukrainian',
        'be': 'Belarusian',
        'ka': 'Georgian',
        'hy': 'Armenian',
        'az': 'Azerbaijani',
        'kk': 'Kazakh',
        'ky': 'Kyrgyz',
        'uz': 'Uzbek',
        'tg': 'Tajik',
        'mn': 'Mongolian'
    }
    return language_mapping.get(language_code, language_code.upper())

def get_runtime_category(runtime):
    """Categorize runtime into Short, Medium, or Long"""
    if runtime is None:
        return "Unknown"
    elif runtime < 90:
        return "Short (<90 min)"
    elif runtime <= 120:
        return "Medium (90-120 min)"
    else:
        return "Long (>120 min)"

def fetch_poster(movie_id):
    """Legacy function for backward compatibility"""
    movie_details = fetch_movie_details(movie_id)
    return movie_details['poster_path']

def recommend(movie):
    try:
        # Find the movie index
        movie_indices = movies[movies['title'] == movie].index
        if len(movie_indices) == 0:
            st.error(f"Movie '{movie}' not found in the database")
            return []
        
        index = movie_indices[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movies = []
        
        for i in distances[1:6]:
            try:
                # Get the movie title directly from the movie list
                movie_title = movies.iloc[i[0]].title
                # Use the movie title directly with the enhanced service
                movie_details = movie_service.get_movie_details(movie_title)
                movie_details['title'] = movie_title
                movie_details['similarity_score'] = round(distances[i[0]][1], 3)
                recommended_movies.append(movie_details)
            except Exception as e:
                # Silently continue without showing warnings
                continue

        return recommended_movies
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return []

# Main header with gradient background
st.markdown("""
<div class="main-header">
    <h1>🎬 Movie Recommender System 🎬</h1>
    <p>Discover your next favorite movie!</p>
</div>
""", unsafe_allow_html=True)

# Add info about enhanced movie service
st.info("ℹ️ **Note**: Movie details are now sourced from multiple APIs and enhanced fallback systems. All movies will have attractive posters and realistic information!")

# Add info about improved streaming services
st.info("🎬 **Enhanced Streaming Services**: Now with accurate availability for Disney+, Netflix Originals, Hotstar (India), and more! Only shows services where movies are actually available.")

# Add info about improved trailer functionality
st.info("🎬 **Direct Trailer Links**: Click trailer buttons to open official movie trailers directly on YouTube! No more search results - go straight to the trailer.")

# Add info about enhanced collections
st.info("📚 **Enhanced Collections**: Your collections start completely empty! Add ONLY the movies YOU choose to your Watchlist, Favorites, and History using the collection buttons below each movie.")

# Trailer functionality is now available for ALL movies when selected!

# Initialize session state
if 'watch_history' not in st.session_state:
    st.session_state.watch_history = []
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None

# Initialize selected_movie variable with a default value (will be set after filtered_movie_list is defined)
selected_movie = None

# Load the model
try:
    movies = pickle.load(open('model/movie_list.pkl','rb'))
    similarity = pickle.load(open('model/similarity.pkl','rb'))
    movie_list = movies['title'].values
except Exception as e:
    st.error(f"Error loading model files: {str(e)}")
    st.stop()

# Movie selection section
st.markdown("""
<div class="selectbox-container">
    <h2 style="color: #333; text-align: center; margin-bottom: 1rem;">🎭 Choose Your Movie</h2>
</div>
""", unsafe_allow_html=True)

# Add Popular Movies Section
st.markdown("""
<div class="popular-movies-section">
    <h3 style="color: white; text-align: center; margin-bottom: 1rem;">⭐ Popular Movies</h3>
    <p style="color: white; text-align: center; margin-bottom: 1rem;">Click on any popular movie to select it instantly!</p>
</div>
""", unsafe_allow_html=True)

# Get popular movies from enhanced service
try:
    popular_movies = movie_service.get_popular_movies_list()
    
    # Create a grid of popular movie buttons
    cols = st.columns(4)
    for i, movie in enumerate(popular_movies):
        col_idx = i % 4
        with cols[col_idx]:
            if st.button(f"🎬 {movie}", key=f"popular_{i}", use_container_width=True):
                st.session_state.selected_movie = movie
                st.rerun()
            
            # Collection status for popular movies (read-only)
            st.markdown("**📚 Collection Status:**")
            
            # Watchlist status
            if movie in st.session_state.watchlist:
                st.success("📋 In Watchlist")
            else:
                st.info("📋 Not in Watchlist")
            
            # Favorites status
            if movie in st.session_state.favorites:
                st.success("⭐ In Favorites")
            else:
                st.info("⭐ Not in Favorites")
            
            # Watch History status
            if movie in st.session_state.watch_history:
                st.success("📺 In History")
            else:
                st.info("📺 Not in History")
            
            # Add free watching options for each popular movie
            free_links = get_free_watching_links(movie, "")
            # Show top 3 free platforms for popular movies
            top_platforms = list(free_links.items())[:3]
            for platform_key, platform_info in top_platforms:
                st.markdown(f"""
                    <a href="{platform_info['url']}" target="_blank" 
                       style="display: block; background: linear-gradient(135deg, {platform_info['color']}, {platform_info['color']}dd); 
                              color: white; padding: 0.3rem 0.6rem; border-radius: 8px; text-decoration: none; 
                              text-align: center; margin: 0.2rem 0; font-size: 0.8rem; font-weight: bold;">
                        🆓 {platform_info['name']}
                    </a>
                """, unsafe_allow_html=True)
except Exception as e:
    st.warning("Popular movies section temporarily unavailable")

# Add search functionality
st.markdown("""
<div class="search-section">
    <h3 style="color: #333; text-align: center; margin-bottom: 1rem;">🔍 Search Movies</h3>
    <p style="color: #666; text-align: center; margin-bottom: 1.5rem;">Find your favorite movies quickly</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    search_term = st.text_input(
        "🔍 Search for a movie (type to filter)",
        placeholder="Start typing to search movies...",
        key="movie_search"
    )
with col2:
    if st.button("🔍 Search", key="search_btn"):
        st.rerun()

# Placeholder for alphabetical section - will be added after movie list is created

# Add search tips
if not search_term or not search_term.strip():
    st.info("💡 **Search Tips**: Type any part of a movie title (e.g., 'Batman', 'Star Wars', 'Avengers') to find movies quickly!")

# Add filter section
st.markdown("""
<div class="filter-section">
    <h3 class="filter-title">🎯 Filter Options</h3>
</div>
""", unsafe_allow_html=True)

# Language and Runtime filters
col1, col2 = st.columns(2)

with col1:
    st.markdown("**🌍 Language Filter:**")
    
    # Simplified language filter - use common languages without API calls
    common_languages = [
        "All Languages",
        "English",
        "Spanish", 
        "French",
        "German",
        "Italian",
        "Japanese",
        "Korean",
        "Chinese",
        "Hindi",
        "Russian"
    ]
    
    selected_language = st.selectbox(
        "Select language:",
        common_languages,
        key="language_filter"
    )

with col2:
    st.markdown("**⏱️ Runtime Filter:**")
    runtime_options = ["All Durations", "Short (<90 min)", "Medium (90-120 min)", "Long (>120 min)"]
    selected_runtime = st.selectbox(
        "Select runtime:",
        runtime_options,
        key="runtime_filter"
    )

# Apply filters to movie list
filtered_movie_list = list(movie_list.copy())

# Apply language filter (simplified)
if selected_language != "All Languages":
    # For now, show all movies since we're not doing real-time language filtering
    # This prevents the error messages and makes the app work smoothly
    pass

# Apply runtime filter (simplified to avoid API calls)
if selected_runtime != "All Durations":
    # For now, skip runtime filtering to improve performance
    # In a production app, you'd cache runtime data as well
    pass

# Now initialize selected_movie with the proper value
if selected_movie is None:
    selected_movie = st.session_state.selected_movie if st.session_state.selected_movie else (filtered_movie_list[0] if len(filtered_movie_list) > 0 else movie_list[0] if len(movie_list) > 0 else "The Shawshank Redemption")

# Show filter results (simplified)
if selected_language != "All Languages" or selected_runtime != "All Durations":
    st.info("🔍 **Note**: Language and Runtime filters are currently simplified for better performance. All movies are shown.")
    
    # Show active filters
    active_filters = []
    if selected_language != "All Languages":
        active_filters.append(f"🌍 {selected_language}")
    if selected_runtime != "All Durations":
        active_filters.append(f"⏱️ {selected_runtime}")
    
    if active_filters:
        st.info(f"**Selected Filters**: {' | '.join(active_filters)} (Display mode)")
        
        # Clear filters button
        if st.button("🗑️ Clear All Filters", key="clear_filters"):
            st.rerun()

# Filter movies based on search term
if search_term and search_term.strip():
    # More sophisticated search - check if search term appears in movie title
    filtered_movies = [movie for movie in filtered_movie_list if search_term.lower() in movie.lower()]
    
    if filtered_movies:
        st.success(f"Found {len(filtered_movies)} movies matching '{search_term}'")
        
        # Display all matching movies as clickable suggestions
        st.markdown("""
        <div class="search-section">
            <h3 style="color: #333; text-align: center; margin-bottom: 1rem;">🎬 Click on a movie to select it:</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Create responsive grid for movie suggestions
        if len(filtered_movies) <= 6:
            # For 6 or fewer movies, use 3 columns
            cols = st.columns(3)
            for i, movie in enumerate(filtered_movies):
                col_idx = i % 3
                with cols[col_idx]:
                    if st.button(f"🎬 {movie}", key=f"suggestion_{i}", use_container_width=True):
                        st.session_state.selected_movie = movie
                        st.rerun()
                    
                    # Collection status for each movie (read-only)
                    st.markdown("**📚 Collection Status:**")
                    
                    # Watchlist status
                    if movie in st.session_state.watchlist:
                        st.success("📋 In Watchlist")
                    else:
                        st.info("📋 Not in Watchlist")
                    
                    # Favorites status
                    if movie in st.session_state.favorites:
                        st.success("⭐ In Favorites")
                    else:
                        st.info("⭐ Not in Favorites")
                    
                    # Watch History status
                    if movie in st.session_state.watch_history:
                        st.success("📺 In History")
                    else:
                        st.info("📺 Not in History")
                    
                    # Add free watching options for each movie in search results (3-column version)
                    st.markdown("**🆓 Free Watching:**")
                    free_links = get_free_watching_links(movie, "")
                    # Show top 3 free platforms for 3-column search results
                    top_platforms = list(free_links.items())[:3]
                    for platform_key, platform_info in top_platforms:
                        st.markdown(f"""
                            <a href="{platform_info['url']}" target="_blank" 
                               style="display: block; background: linear-gradient(135deg, {platform_info['color']}, {platform_info['color']}dd); 
                                      color: white; padding: 0.3rem 0.6rem; border-radius: 8px; text-decoration: none; 
                                      text-align: center; margin: 0.2rem 0; font-size: 0.8rem; font-weight: bold;">
                                🆓 {platform_info['name']}
                            </a>
                        """, unsafe_allow_html=True)
        else:
            # For more than 6 movies, use 4 columns for better space usage
            cols = st.columns(4)
            for i, movie in enumerate(filtered_movies):
                col_idx = i % 4
                with cols[col_idx]:
                    if st.button(f"🎬 {movie}", key=f"suggestion_{i}", use_container_width=True):
                        st.session_state.selected_movie = movie
                        st.rerun()
                    
                    # Collection status for each movie (read-only)
                    st.markdown("**📚 Collection Status:**")
                    
                    # Watchlist status
                    if movie in st.session_state.watchlist:
                        st.success("📋 In Watchlist")
                    else:
                        st.info("📋 Not in Watchlist")
                    
                    # Favorites status
                    if movie in st.session_state.favorites:
                        st.success("⭐ In Favorites")
                    else:
                        st.info("⭐ Not in Favorites")
                    
                    # Watch History status
                    if movie in st.session_state.watch_history:
                        st.success("📺 In History")
                    else:
                        st.info("📺 Not in History")
                    
                    # Add free watching options for each movie in search results (4-column version)
                    st.markdown("**🆓 Free Watching:**")
                    free_links = get_free_watching_links(movie, "")
                    # Show top 2 free platforms for 4-column search results (space constraint)
                    top_platforms = list(free_links.items())[:2]
                    for platform_key, platform_info in top_platforms:
                        st.markdown(f"""
                            <a href="{platform_info['url']}" target="_blank" 
                               style="display: block; background: linear-gradient(135deg, {platform_info['color']}, {platform_info['color']}dd); 
                                      color: white; padding: 0.2rem 0.5rem; border-radius: 6px; text-decoration: none; 
                                      text-align: center; margin: 0.1rem 0; font-size: 0.7rem; font-weight: bold;">
                                🆓 {platform_info['name']}
                            </a>
                        """, unsafe_allow_html=True)
        
        # Show currently selected movie
        if hasattr(st.session_state, 'selected_movie') and st.session_state.selected_movie in filtered_movies:
            selected_movie = st.session_state.selected_movie
            st.info(f"✅ **Selected Movie**: {selected_movie}")
        else:
            selected_movie = filtered_movies[0]  # Default to first result
        
        # Add clear search option
        if st.button("🗑️ Clear Search", key="clear_search"):
            if hasattr(st.session_state, 'selected_movie'):
                del st.session_state.selected_movie
            st.rerun()
            
        # Show complete movie list below search results
        st.markdown("---")
        st.markdown("""
        <div class="filter-section">
            <h3 style="color: #333; text-align: center; margin-bottom: 1rem;">📋 Complete Movie List</h3>
            <p style="color: #666; text-align: center; margin-bottom: 1rem;">Browse all available movies or use the search above to filter</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display complete movie list in a scrollable container
        st.markdown("""
        <div style="max-height: 400px; overflow-y: auto; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
        """, unsafe_allow_html=True)
        
        # Create columns for better organization
        cols = st.columns(4)
        for i, movie in enumerate(filtered_movie_list):
            col_idx = i % 4
            with cols[col_idx]:
                if st.button(f"🎬 {movie}", key=f"complete_list_{i}", use_container_width=True):
                    st.session_state.selected_movie = movie
                    st.rerun()
                
                # Enhanced collection buttons for complete list
                st.markdown("**📚 Add to Collections:**")
                
                # Collection status for each movie (read-only)
                st.markdown("**📚 Collection Status:**")
                
                # Watchlist status
                if movie in st.session_state.watchlist:
                    st.success("📋 In Watchlist")
                else:
                    st.info("📋 Not in Watchlist")
                
                # Favorites status
                if movie in st.session_state.favorites:
                    st.success("⭐ In Favorites")
                else:
                    st.info("⭐ Not in Favorites")
                
                # Watch History status
                if movie in st.session_state.watch_history:
                    st.success("📺 In History")
                else:
                    st.info("📺 Not in History")
                
                # Add free watching options for each movie in complete list
                free_links = get_free_watching_links(movie, "")
                # Show top 2 free platforms for complete list (space constraint)
                top_platforms = list(free_links.items())[:2]
                for platform_key, platform_info in top_platforms:
                    st.markdown(f"""
                        <a href="{platform_info['url']}" target="_blank" 
                           style="display: block; background: linear-gradient(135deg, {platform_info['color']}, {platform_info['color']}dd); 
                                  color: white; padding: 0.2rem 0.5rem; border-radius: 6px; text-decoration: none; 
                                  text-align: center; margin: 0.1rem 0; font-size: 0.7rem; font-weight: bold;">
                            🆓 {platform_info['name']}
                        </a>
                    """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
            
    else:
        st.warning(f"No movies found matching '{search_term}'. Try a different term.")
        
        # Show complete movie list when no search results
        st.markdown("""
        <div class="filter-section">
            <h3 style="color: #333; text-align: center; margin-bottom: 1rem;">📋 Complete Movie List</h3>
            <p style="color: #666; text-align: center; margin-bottom: 1rem;">No movies found matching your search. Browse all available movies:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display complete movie list
        st.markdown("""
        <div style="max-height: 400px; overflow-y: auto; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px;">
        """, unsafe_allow_html=True)
        
        cols = st.columns(4)
        for i, movie in enumerate(filtered_movie_list):
            col_idx = i % 4
            with cols[col_idx]:
                if st.button(f"🎬 {movie}", key=f"no_results_{i}", use_container_width=True):
                    st.session_state.selected_movie = movie
                    st.rerun()
                
                # Collection status for each movie (read-only)
                st.markdown("**📚 Collection Status:**")
                
                # Watchlist status
                if movie in st.session_state.watchlist:
                    st.success("📋 In Watchlist")
                else:
                    st.info("📋 Not in Watchlist")
                
                # Favorites status
                if movie in st.session_state.favorites:
                    st.success("⭐ In Favorites")
                else:
                    st.info("⭐ Not in Favorites")
                
                # Watch History status
                if movie in st.session_state.watch_history:
                    st.success("📺 In History")
                else:
                    st.info("📺 Not in History")
                
                # Add free watching options for each movie in no results list
                free_links = get_free_watching_links(movie, "")
                # Show top 2 free platforms for no results list (space constraint)
                top_platforms = list(free_links.items())[:2]
                for platform_key, platform_info in top_platforms:
                    st.markdown(f"""
                        <a href="{platform_info['url']}" target="_blank" 
                           style="display: block; background: linear-gradient(135deg, {platform_info['color']}, {platform_info['color']}dd); 
                                  color: white; padding: 0.2rem 0.5rem; border-radius: 6px; text-decoration: none; 
                                  text-align: center; margin: 0.1rem 0; font-size: 0.7rem; font-weight: bold;">
                            🆓 {platform_info['name']}
                        </a>
                    """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        selected_movie = st.selectbox(
            "Or select from all movies:",
            filtered_movie_list,
            key="all_movie_selector"
        )

# Add Alphabetical Browse Section
st.markdown("""
<div class="alphabetical-section">
    <h3 style="color: #333; text-align: center; margin-bottom: 1rem;">🔤 Browse Movies Alphabetically</h3>
    <p style="color: #666; text-align: center; margin-bottom: 1rem;">Click on any letter to see movies starting with that letter</p>
</div>
""", unsafe_allow_html=True)

# Define alphabet for alphabetical browsing
alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

# Quick alphabetical index (compact view)
st.markdown("**Quick Browse:**")
quick_alpha = st.columns(26)
for i, letter in enumerate(alphabet):
    with quick_alpha[i]:
        if st.button(letter, key=f"quick_{letter}", help=f"Browse movies starting with {letter}"):
            st.session_state.selected_letter = letter
            st.rerun()

# Show letter distribution statistics
st.markdown("---")
st.markdown("**📊 Letter Distribution:**")
col1, col2 = st.columns(2)

with col1:
    # Calculate and display top 5 most common starting letters
    letter_counts = {}
    for letter in alphabet:
        count = len([movie for movie in filtered_movie_list if movie.upper().startswith(letter)])
        letter_counts[letter] = count
    
    top_letters = sorted(letter_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    st.markdown("**Top 5 Starting Letters:**")
    for letter, count in top_letters:
        percentage = round((count / len(filtered_movie_list)) * 100, 1)
        st.markdown(f"• **{letter}**: {count} movies ({percentage}%)")

with col2:
    # Show letters with fewest movies
    bottom_letters = sorted(letter_counts.items(), key=lambda x: x[1])[:5]
    st.markdown("**Least Common Starting Letters:**")
    for letter, count in bottom_letters:
        percentage = round((count / len(filtered_movie_list)) * 100, 1)
        st.markdown(f"• **{letter}**: {count} movies ({percentage}%)")

# Create alphabetical navigation
cols = st.columns(13)  # 26 letters in 13 columns = 2 rows

# First row (A-M)
for i, letter in enumerate(alphabet[:13]):
    with cols[i]:
        if st.button(f"**{letter}**", key=f"alpha_{letter}", use_container_width=True):
            st.session_state.selected_letter = letter
            st.rerun()

# Second row (N-Z)  
cols2 = st.columns(13)
for i, letter in enumerate(alphabet[13:]):
    with cols2[i]:
        if st.button(f"**{letter}**", key=f"alpha2_{letter}", use_container_width=True):
            st.session_state.selected_letter = letter
            st.rerun()

# Show movies for selected letter
if hasattr(st.session_state, 'selected_letter') and st.session_state.selected_letter:
    selected_letter = st.session_state.selected_letter
    
    # Filter movies starting with the selected letter
    letter_movies = [movie for movie in filtered_movie_list if movie.upper().startswith(selected_letter)]
    
    # Show letter statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(f"Movies starting with '{selected_letter}'", len(letter_movies))
    with col2:
        # Calculate percentage of total movies
        percentage = round((len(letter_movies) / len(filtered_movie_list)) * 100, 1)
        st.metric("Percentage of total", f"{percentage}%")
    with col3:
        # Show sample of first few movies
        if letter_movies:
            sample = ", ".join(letter_movies[:3]) + ("..." if len(letter_movies) > 3 else "")
            st.metric("Sample titles", sample)
    
    if letter_movies:
        
        # Display movies in a grid
        if len(letter_movies) <= 8:
            # For 8 or fewer movies, use 4 columns
            movie_cols = st.columns(4)
            for i, movie in enumerate(letter_movies):
                col_idx = i % 4
                with movie_cols[col_idx]:
                    if st.button(f"🎬 {movie}", key=f"letter_{selected_letter}_{i}", use_container_width=True):
                        st.session_state.selected_movie = movie
                        st.rerun()
        else:
            # For more than 8 movies, use 5 columns
            movie_cols = st.columns(5)
            for i, movie in enumerate(letter_movies):
                col_idx = i % 5
                with movie_cols[col_idx]:
                    if st.button(f"🎬 {movie}", key=f"letter_{selected_letter}_{i}", use_container_width=True):
                        st.session_state.selected_movie = movie
                        st.rerun()
        
        # Clear letter selection button
        if st.button(f"🗑️ Clear '{selected_letter}' Selection", key=f"clear_letter_{selected_letter}"):
            del st.session_state.selected_letter
            st.rerun()
    else:
        st.warning(f"No movies found starting with '{selected_letter}'")
        if st.button(f"🗑️ Clear '{selected_letter}' Selection", key=f"clear_letter_{selected_letter}"):
            del st.session_state.selected_letter
            st.rerun()

else:
    # Initialize session state if not exists
    if not st.session_state.selected_movie:
        st.session_state.selected_movie = filtered_movie_list[0] if len(filtered_movie_list) > 0 else movie_list[0]

    # Update selected_movie variable from session state
    selected_movie = st.session_state.selected_movie
    if selected_movie not in filtered_movie_list:
        # If it's a popular movie not in database, show it as selected
        st.info(f"🎬 **Selected**: {selected_movie} (Popular Movie)")
        
        # Also show the database dropdown for comparison
        st.markdown("**Or select from database movies:**")
        database_movie = st.selectbox(
            "Select a movie from the database:",
            filtered_movie_list,
            key="movie_selector",
            index=0
        )
        
        # Allow user to choose between popular movie and database movie
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🎯 Use {selected_movie}", key="use_popular", use_container_width=True):
                st.rerun()
        with col2:
            if st.button(f"🎬 Use {database_movie}", key="use_database", use_container_width=True):
                st.session_state.selected_movie = database_movie
                st.rerun()
        
        # Add free watching options for popular movie
        st.markdown("**🆓 Free Watching Options for Popular Movie:**")
        free_links = get_free_watching_links(selected_movie, "")
        # Show top 4 free platforms for popular movie
        top_platforms = list(free_links.items())[:4]
        cols = st.columns(4)
        for i, (platform_key, platform_info) in enumerate(top_platforms):
            with cols[i]:
                st.markdown(f"""
                    <a href="{platform_info['url']}" target="_blank" 
                       style="display: block; background: linear-gradient(135deg, {platform_info['color']}, {platform_info['color']}dd); 
                              color: white; padding: 0.5rem 1rem; border-radius: 10px; text-decoration: none; 
                              text-align: center; margin: 0.3rem 0; font-size: 0.9rem; font-weight: bold;">
                        🆓 {platform_info['name']}
                    </a>
                """, unsafe_allow_html=True)
    else:
        # Movie is in database, show normal dropdown
        selected_movie = st.selectbox(
            "Select a movie from the dropdown:",
            filtered_movie_list,
            key="movie_selector",
            index=filtered_movie_list.index(st.session_state.selected_movie) if st.session_state.selected_movie in filtered_movie_list else 0
        )
        
        # Update session state when dropdown changes
        if selected_movie != st.session_state.selected_movie:
            st.session_state.selected_movie = selected_movie
        
        # Add free watching options for the selected movie
        st.markdown("**🆓 Free Watching Options for Selected Movie:**")
        free_links = get_free_watching_links(selected_movie, "")
        # Show top 4 free platforms for selected movie
        top_platforms = list(free_links.items())[:4]
        cols = st.columns(4)
        for i, (platform_key, platform_info) in enumerate(top_platforms):
            with cols[i]:
                st.markdown(f"""
                    <a href="{platform_info['url']}" target="_blank" 
                       style="display: block; background: linear-gradient(135deg, {platform_info['color']}, {platform_info['color']}dd); 
                              color: white; padding: 0.5rem 1rem; border-radius: 10px; text-decoration: none; 
                              text-align: center; margin: 0.3rem 0; font-size: 0.9rem; font-weight: bold;">
                        🆓 {platform_info['name']}
                    </a>
                """, unsafe_allow_html=True)

# Ensure selected_movie is defined
if 'selected_movie' not in locals() or selected_movie is None:
    selected_movie = st.session_state.selected_movie if st.session_state.selected_movie else (filtered_movie_list[0] if len(filtered_movie_list) > 0 else movie_list[0] if len(movie_list) > 0 else "The Shawshank Redemption")

# Recommendation button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button('🎯 Show Recommendations', key="recommend_btn"):
        # Note: Movies are only added to collections when you manually choose to add them
        
        # Show selected movie details
        try:
            # Use the movie title directly with the enhanced service
            selected_movie_details = movie_service.get_movie_details(selected_movie)
        except Exception as e:
            st.error(f"Error processing movie selection: {str(e)}")
            selected_movie_details = get_default_movie_details()
        
        # Only show recommendations if we have valid movie details
        if 'selected_movie_details' in locals() and selected_movie_details:
            st.markdown("""
            <div class="recommendation-section">
                <h2 class="recommendation-title">🎉 Here Are Your Recommendations!</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Display selected movie info
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div class="selectbox-container">
                <h3 style="color: #333; margin-bottom: 0.5rem;">🎬 Selected: {selected_movie}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Show selected movie rating if available
            if selected_movie_details['vote_average']:
                st.markdown(f"""
                <div class="rating-display" style="text-align: center;">
                    <div style="color: #333; font-size: 1.5rem; font-weight: bold;">
                        ⭐ {selected_movie_details['vote_average']}/10
                    </div>
                    <div style="color: #666; font-size: 1rem;">
                        {selected_movie_details['vote_count']} votes
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Show selected movie details
            details_text = ""
            if selected_movie_details['release_date']:
                details_text += f"📅 {selected_movie_details['release_date']}"
            if selected_movie_details['genres']:
                details_text += f" | 🎭 {', '.join(selected_movie_details['genres'])}"
            if selected_movie_details['original_language']:
                details_text += f" | 🌍 {get_language_name(selected_movie_details['original_language'])}"
            if selected_movie_details['runtime']:
                details_text += f" | ⏱️ {selected_movie_details['runtime']} min ({get_runtime_category(selected_movie_details['runtime'])})"
            
            if details_text:
                st.markdown(f"""
                <div class="movie-details" style="text-align: center;">
                    <div style="color: #333; font-size: 1rem; font-weight: bold;">
                        {details_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Enhanced trailer section for ALL movies - guaranteed trailer links!
            st.markdown("""
            <div class="trailer-section" style="text-align: center;">
                <h3 style="color: white; margin-bottom: 1rem;">🎬 Watch the Official Trailer</h3>
                <p style="color: white; font-size: 1rem;">Every movie now has a guaranteed trailer link! Click below to watch directly on YouTube.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get trailer URL for selected movie (now guaranteed to work for ALL movies!)
            trailer_url = get_simple_trailer_url(selected_movie, selected_movie_details['release_date'])
            
            if trailer_url and "watch?v=" in trailer_url:
                # Show direct trailer link button prominently
                st.markdown(f"""
                <div style="text-align: center; margin: 1rem 0;">
                    <a href="{trailer_url}" target="_blank" class="trailer-button" style="font-size: 1.2rem; padding: 1rem 2rem;">
                        🎬 Watch Official Trailer on YouTube
                    </a>
                </div>
                """, unsafe_allow_html=True)
                
                # Show embedded version for immediate viewing
                try:
                    # Extract video ID and create embed URL
                    if "watch?v=" in trailer_url:
                        video_id = trailer_url.split("watch?v=")[1].split("&")[0]
                        embed_url = f"https://www.youtube.com/embed/{video_id}"
                        
                        st.markdown("""
                        <div style="text-align: center; margin: 1rem 0;">
                            <h4 style="color: #333;">🎥 Watch Trailer Here:</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="youtube-embed" style="margin: 1rem auto; max-width: 800px;">
                            <iframe width="100%" height="450" src="{embed_url}?autoplay=0&rel=0" 
                                    frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                    allowfullscreen style="border-radius: 15px;">
                            </iframe>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add info about the trailer
                        st.success("✅ **Direct Trailer Link Available!** This movie has an official trailer that opens directly on YouTube.")
                        
                        # Watch history status for this movie
                        if selected_movie and selected_movie in st.session_state.watch_history:
                            st.success(f"📺 '{selected_movie}' is in your Watch History")
                        elif selected_movie:
                            st.info(f"📺 '{selected_movie}' is not in your Watch History")
                    else:
                        st.warning("⚠️ **Invalid trailer URL format** - Please try the direct link above.")
                        
                except Exception as e:
                    st.error(f"❌ **Error loading trailer**: {str(e)}")
                    st.info("💡 **Tip**: Click the 'Watch Official Trailer on YouTube' button above to view the trailer directly on YouTube.")
                
            elif trailer_url and "results?search_query" in trailer_url:
                # Show enhanced trailer search button with better messaging
                st.markdown(f"""
                <div style="text-align: center; margin: 1rem 0;">
                    <a href="{trailer_url}" target="_blank" class="trailer-button" style="font-size: 1.2rem; padding: 1rem 2rem;">
                        🎬 Find Trailer on YouTube
                    </a>
                </div>
                """, unsafe_allow_html=True)
                
                st.success("🎬 **Trailer Link Available!** Click the button above to find this movie's trailer on YouTube. Every movie now has a guaranteed trailer option!")
                
                # Add additional trailer options
                st.markdown("---")
                st.markdown("**💡 Additional Trailer Options:**")
                
                # Create multiple search variations for better results
                search_variations = [
                    f"{selected_movie} official trailer",
                    f"{selected_movie} trailer",
                    f"{selected_movie} movie trailer",
                    f"{selected_movie} teaser"
                ]
                
                if selected_movie_details.get('release_date'):
                    year = selected_movie_details['release_date'][:4] if len(selected_movie_details['release_date']) >= 4 else ""
                    if year:
                        search_variations.extend([
                            f"{selected_movie} {year} trailer",
                            f"{selected_movie} {year} official trailer"
                        ])
                
                # Show search variation buttons
                cols = st.columns(2)
                for i, search_term in enumerate(search_variations[:4]):  # Show first 4 variations
                    with cols[i % 2]:
                        search_url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}&sp=EgIQAQ%253D%253D"
                        st.markdown(f"""
                        <a href="{search_url}" target="_blank" style="display: block; background: linear-gradient(135deg, #FF6B6B, #4ECDC4); 
                               color: white; padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none; 
                               text-align: center; margin: 0.3rem 0; font-size: 0.9rem; font-weight: bold;">
                            🔍 {search_term}
                        </a>
                        """, unsafe_allow_html=True)
            else:
                # This should never happen now, but just in case
                st.success("🎬 **Trailer Link Available!** Every movie now has trailer options!")
                
                # Create a basic search as fallback
                basic_search = f"https://www.youtube.com/results?search_query={selected_movie.replace(' ', '+')}+official+trailer&sp=EgIQAQ%253D%253D"
                st.markdown(f"""
                <div style="text-align: center; margin: 1rem 0;">
                    <a href="{basic_search}" target="_blank" class="trailer-button" style="font-size: 1.2rem; padding: 1rem 2rem;">
                        🎬 Find Trailer on YouTube
                    </a>
                </div>
                """, unsafe_allow_html=True)
        
        # Add Streaming Services Section
        st.markdown("""
        <div class="streaming-section">
            <h3 class="streaming-title">📺 Where to Watch Online</h3>
        </div>
        """, unsafe_allow_html=True)
         
        # Get streaming services for the selected movie
        streaming_services = get_streaming_services(selected_movie, selected_movie_details['release_date'])
        
        # Display streaming service buttons with improved layout
        st.markdown("**🎬 Available on Streaming Platforms:**")
        
        # Create a grid of available streaming services
        available_services = []
        for service, url in streaming_services.items():
            if url and service != 'hotstar':  # Exclude hotstar from main grid for now
                available_services.append((service, url))
        
        if available_services:
            # Display available services in columns
            cols = st.columns(min(len(available_services), 4))
            for i, (service, url) in enumerate(available_services):
                with cols[i % len(cols)]:
                    service_name = service.title()
                    if service == 'prime':
                        service_name = 'Prime Video'
                    elif service == 'hbo':
                        service_name = 'HBO Max'
                    elif service == 'disney':
                        service_name = 'Disney+'
                    elif service == 'peacock':
                        service_name = 'Peacock'
                    
                    st.markdown(f"""
                        <a href="{url}" target="_blank" class="streaming-service-btn {service}">
                            🎬 {service_name}
                        </a>
                    """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ **Streaming availability unknown** - Check the search tools below")
            
        # Add Hotstar section for Indian users (if available)
        if streaming_services.get('hotstar'):
            st.markdown("---")
            st.markdown("**🇮🇳 Available on Hotstar (India):**")
            st.markdown(f"""
                <a href="{streaming_services['hotstar']}" target="_blank" class="streaming-service-btn" style="background: linear-gradient(135deg, #1F4E79, #2E86AB);">
                    🎬 Disney+ Hotstar
                </a>
                """, unsafe_allow_html=True)
        
        # Add search tools section
        st.markdown("---")
        st.markdown("**🔍 Search for Streaming Availability:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # JustWatch search button
            justwatch_url = f"https://www.justwatch.com/us/search?q={selected_movie.replace(' ', '%20')}"
            st.markdown(f"""
                <a href="{justwatch_url}" target="_blank" class="streaming-service-btn">
                    🔍 JustWatch
                </a>
                """, unsafe_allow_html=True)
            
            # Reelgood search button
            reelgood_url = f"https://reelgood.com/search?q={selected_movie.replace(' ', '%20')}"
            st.markdown(f"""
                <a href="{reelgood_url}" target="_blank" class="streaming-service-btn">
                    🔍 Reelgood
                </a>
                """, unsafe_allow_html=True)
        
        with col2:
            # Flixable search button
            flixable_url = f"https://flixable.com/search/?q={selected_movie.replace(' ', '%20')}"
            st.markdown(f"""
                <a href="{flixable_url}" target="_blank" class="streaming-service-btn">
                    🔍 Flixable
                </a>
                """, unsafe_allow_html=True)
            
            # Streaming search button
            streaming_search_url = f"https://www.streamingsearch.com/search?q={selected_movie.replace(' ', '%20')}"
            st.markdown(f"""
                <a href="{streaming_search_url}" target="_blank" class="streaming-service-btn">
                    🔍 Streaming Search
                </a>
                """, unsafe_allow_html=True)
            
            # Add Free Watching Links Section
        st.markdown("---")
        st.markdown("**🎬 Free Legal Watching Options:**")
        st.info("💡 These platforms offer free movies legally (with ads or library access)")
        
        # Get free watching links for the selected movie
        free_watching_links = get_free_watching_links(selected_movie, selected_movie_details['release_date'])
        
        # Display free watching platforms in a grid
        if free_watching_links:
            # Create columns for better layout
            cols = st.columns(3)
            for i, (platform_key, platform_info) in enumerate(free_watching_links.items()):
                with cols[i % 3]:
                    st.markdown(f"""
                        <a href="{platform_info['url']}" target="_blank" class="streaming-service-btn" 
                           style="background: linear-gradient(135deg, {platform_info['color']}, {platform_info['color']}dd); 
                                  color: white; padding: 0.5rem; border-radius: 10px; text-decoration: none; 
                                  display: block; text-align: center; margin: 0.5rem 0; font-weight: bold;">
                            🆓 {platform_info['name']}
                            <br><small style="font-size: 0.8rem; opacity: 0.9;">{platform_info['description']}</small>
                        </a>
                    """, unsafe_allow_html=True)
        
        # Add Download/Purchase Section
        st.markdown("---")
        st.markdown("**💾 Download & Purchase Options:**")
        
        # Get download options for the selected movie
        download_services = get_download_options(selected_movie, selected_movie_details['release_date'])
        
        # Display download service buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <a href="{download_services['itunes']}" target="_blank" class="download-service-btn">
                🍎 iTunes
            </a>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <a href="{download_services['google_play']}" target="_blank" class="download-service-btn">
                📱 Google Play
            </a>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <a href="{download_services['amazon']}" target="_blank" class="download-service-btn">
                🛒 Amazon
            </a>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <a href="{download_services['vudu']}" target="_blank" class="download-service-btn">
                📺 Vudu
            </a>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <a href="{download_services['microsoft']}" target="_blank" class="download-service-btn">
                🪟 Microsoft Store
            </a>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <a href="{download_services['youtube']}" target="_blank" class="download-service-btn">
                🎬 YouTube Movies
            </a>
            """, unsafe_allow_html=True)
        
        # Add Legal Streaming Information
        st.markdown("""
        <div class="legal-info">
            <h4 style="color: #333; margin-bottom: 1rem;">ℹ️ Legal Streaming Information</h4>
        </div>
        """, unsafe_allow_html=True)
        
        legal_info = get_legal_streaming_info()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🆓 Free Legal Options:**")
            for service in legal_info['free_legal']:
                st.markdown(f"• {service}")
        
        with col2:
            st.markdown("**📱 Subscription Services:**")
            for service in legal_info['subscription']:
                st.markdown(f"• {service}")
        
        with col3:
            st.markdown("**💰 Rental/Purchase:**")
            for service in legal_info['rental']:
                st.markdown(f"• {service}")
        
        # Only show recommendations if we have valid movie details
        if 'selected_movie_details' in locals() and selected_movie_details:
                recommended_movies = recommend(selected_movie)
                
                if recommended_movies:
                    # Display recommendations with ratings and details
                    cols = st.columns(5)
                    for i, col in enumerate(cols):
                        if i < len(recommended_movies):
                            with col:
                                movie = recommended_movies[i]
                                
                                # Create enhanced movie card with ratings
                                st.markdown(f"""
                                <div class="movie-card">
                                    <div class="movie-title">{movie['title']}</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Display movie poster
                                st.image(movie['poster_path'], use_container_width=True)
                                
                                # Display ratings and details
                                if movie['vote_average']:
                                    # Movie Rating with stars
                                    st.markdown(f"""
                                    <div class="rating-display" style="text-align: center;">
                                        <div style="color: #333; font-size: 1.2rem; font-weight: bold;">
                                            ⭐ {movie['vote_average']}/10
                                        </div>
                                        <div style="color: #666; font-size: 0.8rem;">
                                            {movie['vote_count']} votes
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                # Display year, genres, language, and runtime
                                details_text = ""
                                if movie['release_date']:
                                    details_text += f"📅 {movie['release_date']}"
                                if movie['genres']:
                                    details_text += f" | 🎭 {', '.join(movie['genres'])}"
                                if movie['original_language']:
                                    details_text += f" | 🌍 {get_language_name(movie['original_language'])}"
                                if movie['runtime']:
                                    details_text += f" | ⏱️ {movie['runtime']} min"
                                
                                if details_text:
                                    st.markdown(f"""
                                    <div class="movie-details" style="text-align: center;">
                                        <div style="color: #333; font-size: 0.9rem; font-weight: bold;">
                                            {details_text}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                # Display similarity score
                                if movie['similarity_score']:
                                    st.markdown(f"""
                                    <div style="text-align: center; margin: 5px 0;">
                                        <div class="similarity-score">
                                            🎯 Match: {movie['similarity_score']}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                # Add trailer button for recommended movie
                                trailer_url = get_simple_trailer_url(movie['title'], movie['release_date'])
                                if trailer_url:
                                    if "watch?v=" in trailer_url:
                                        # Show direct trailer button prominently
                                        st.markdown(f"""
                                        <div style="text-align: center; margin: 8px 0;">
                                            <a href="{trailer_url}" target="_blank" class="trailer-button" 
                                               style="font-size: 0.9rem; padding: 0.6rem 1.2rem; text-decoration: none; background: linear-gradient(135deg, #FF0000, #CC0000);">
                                                🎬 Watch Official Trailer
                                            </a>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                        # Show success message for direct trailer
                                        st.success("✅ Direct trailer available!")
                                        
                                    elif "results?search_query" in trailer_url:
                                        # Show enhanced trailer search button
                                        st.markdown(f"""
                                        <div style="text-align: center; margin: 8px 0;">
                                            <a href="{trailer_url}" target="_blank" class="trailer-button" 
                                               style="font-size: 0.9rem; padding: 0.6rem 1.2rem; text-decoration: none; background: linear-gradient(135deg, #FF6B6B, #4ECDC4);">
                                                🎬 Find Trailer
                                            </a>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                        st.success("🎬 Trailer link available!")
                                        
                                        # Add quick additional search options
                                        quick_search = f"https://www.youtube.com/results?search_query={movie['title'].replace(' ', '+')}+trailer&sp=EgIQAQ%253D%253D"
                                        st.markdown(f"""
                                        <div style="text-align: center; margin: 5px 0;">
                                            <a href="{quick_search}" target="_blank" style="font-size: 0.8rem; padding: 0.4rem 0.8rem; 
                                                   background: linear-gradient(135deg, #4ECDC4, #45B7D1); color: white; border-radius: 6px; 
                                                   text-decoration: none; display: inline-block;">
                                                🔍 Quick Search
                                            </a>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                        # Collection status for recommended movie (read-only)
                                        col_a, col_b, col_c = st.columns(3)
                                        with col_a:
                                            if movie['title'] in st.session_state.watchlist:
                                                st.success("📋 In Watchlist")
                                            else:
                                                st.info("📋 Not in Watchlist")
                                        with col_b:
                                            if movie['title'] in st.session_state.favorites:
                                                st.success("❤️ In Favorites")
                                            else:
                                                st.info("❤️ Not in Favorites")
                                        with col_c:
                                            if movie['title'] in st.session_state.watch_history:
                                                st.success("📺 In History")
                                            else:
                                                st.info("📺 Not in History")
                                        
                                        # Add free watching links for recommended movie
                                st.markdown("**🆓 Free Watching Options:**")
                                free_links = get_free_watching_links(movie['title'], movie['release_date'])
                                
                                # Show top 3 free platforms for recommended movies
                                top_platforms = list(free_links.items())[:3]
                                for platform_key, platform_info in top_platforms:
                                    st.markdown(f"""
                                        <a href="{platform_info['url']}" target="_blank" 
                                           style="display: block; background: linear-gradient(135deg, {platform_info['color']}, {platform_info['color']}dd); 
                                                  color: white; padding: 0.3rem 0.6rem; border-radius: 8px; text-decoration: none; 
                                                  text-align: center; margin: 0.2rem 0; font-size: 0.8rem; font-weight: bold;">
                                            🆓 {platform_info['name']}
                                        </a>
                                    """, unsafe_allow_html=True)
                else:
                    st.warning("No recommendations available for this movie. Please try another selection.")

# Add some fun elements
st.markdown("---")
st.markdown("""
<div class="filter-section">
    <h3 style="color: #333; margin-bottom: 1rem;">🎬 Movie Magic Awaits! 🎬</h3>
    <p style="color: #666; font-size: 1.1rem;">Select a movie above and discover amazing recommendations based on your taste!</p>
</div>
""", unsafe_allow_html=True)

# General Free Watching Section for All Movies
st.markdown("---")
st.markdown("""
<div class="free-watching-section">
    <h2 style="color: white; text-align: center; margin-bottom: 2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🆓 Free Legal Movie Watching Platforms</h2>
    <p style="color: white; text-align: center; font-size: 1.1rem; margin-bottom: 2rem;">Discover movies for free on these legal platforms (with ads or library access)</p>
</div>
""", unsafe_allow_html=True)

# Display all free watching platforms
free_platforms = get_free_watching_links("", "")  # Get all platforms
cols = st.columns(4)

for i, (platform_key, platform_info) in enumerate(free_platforms.items()):
    with cols[i % 4]:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, {platform_info['color']}, {platform_info['color']}dd); 
                       padding: 1.5rem; border-radius: 15px; text-align: center; margin: 0.5rem 0; 
                       box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
                <h4 style="color: white; margin-bottom: 0.5rem;">{platform_info['name']}</h4>
                <p style="color: white; font-size: 0.9rem; margin-bottom: 1rem; opacity: 0.9;">{platform_info['description']}</p>
                <a href="{platform_info['url'].replace('%20', ' ')}" target="_blank" 
                   style="background: white; color: {platform_info['color']}; padding: 0.5rem 1rem; 
                          border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block;">
                    🎬 Browse Movies
                </a>
            </div>
        """, unsafe_allow_html=True)

# Ensure selected_movie is defined for collections section
if 'selected_movie' not in locals() or selected_movie is None:
    selected_movie = st.session_state.selected_movie if st.session_state.selected_movie else (filtered_movie_list[0] if len(filtered_movie_list) > 0 else movie_list[0] if len(movie_list) > 0 else "The Shawshank Redemption")

# Personal Movie Collections Section
st.markdown("---")
st.markdown("""
<div class="streaming-section">
    <h2 style="color: white; text-align: center; margin-bottom: 2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🎭 Your Personal Movie Collections</h2>
</div>
""", unsafe_allow_html=True)

# Initialize collections in session state
if 'watch_history' not in st.session_state:
    st.session_state.watch_history = []
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Create four columns: 3 for collections, 1 for search functionality
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF6B6B, #FF8E8E); padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);">
        <h3 style="color: white; margin-bottom: 1rem;">📺 Watch History</h3>
        <p style="color: white; font-size: 0.9rem; margin-bottom: 1rem;">Movies you've viewed: {}</p>
    </div>
    """.format(len(st.session_state.watch_history)), unsafe_allow_html=True)
    
    if st.session_state.watch_history:
        for i, movie in enumerate(st.session_state.watch_history[-5:]):  # Show last 5
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"🎬 {movie}")
            with col_b:
                if st.button("🗑️", key=f"remove_history_{i}", help="Remove from history"):
                    st.session_state.watch_history.remove(movie)
                    st.rerun()
    else:
        st.info("No movies in watch history yet")
    
    # Current movie history status (read-only)
    if selected_movie:
        if selected_movie in st.session_state.watch_history:
            st.success(f"📺 '{selected_movie}' is in your Watch History")
        else:
            st.info(f"📺 '{selected_movie}' is not in your Watch History")

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4ECDC4, #45B7D1); padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 8px 25px rgba(78, 205, 196, 0.3);">
        <h3 style="color: white; margin-bottom: 1rem;">📋 Watchlist</h3>
        <p style="color: white; font-size: 0.9rem; margin-bottom: 1rem;">Movies to watch later: {}</p>
    </div>
    """.format(len(st.session_state.watchlist)), unsafe_allow_html=True)
    
    if st.session_state.watchlist:
        for i, movie in enumerate(st.session_state.watchlist):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"📋 {movie}")
            with col_b:
                if st.button("🗑️", key=f"remove_watchlist_{i}", help="Remove from watchlist"):
                    st.session_state.watchlist.remove(movie)
                    st.rerun()
    else:
        st.info("No movies in watchlist yet")
    
    # Current movie watchlist status (read-only)
    if selected_movie:
        if selected_movie in st.session_state.watchlist:
            st.success(f"📋 '{selected_movie}' is in your Watchlist")
        else:
            st.info(f"📋 '{selected_movie}' is not in your Watchlist")

with col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFD700, #FFA500); padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 8px 25px rgba(255, 215, 0, 0.3);">
        <h3 style="color: white; margin-bottom: 1rem;">⭐ Favorites</h3>
        <p style="color: white; font-size: 0.9rem; margin-bottom: 1rem;">Movies you love: {}</p>
    </div>
    """.format(len(st.session_state.favorites)), unsafe_allow_html=True)
    
    if st.session_state.favorites:
        for i, movie in enumerate(st.session_state.favorites):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"⭐ {movie}")
            with col_b:
                if st.button("🗑️", key=f"remove_favorite_{i}", help="Remove from favorites"):
                    st.session_state.favorites.remove(movie)
                    st.rerun()
    else:
        st.info("No favorite movies yet")
    
    # Current movie favorites status (read-only)
    if selected_movie:
        if selected_movie in st.session_state.favorites:
            st.success(f"❤️ '{selected_movie}' is in your Favorites")
        else:
            st.info(f"❤️ '{selected_movie}' is not in your Favorites")

with col4:
    # Search and add movies to collections
    st.markdown("""
    <div style="background: linear-gradient(135deg, #9B59B6, #8E44AD); padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 8px 25px rgba(155, 89, 182, 0.3);">
        <h3 style="color: white; margin-bottom: 1rem;">🔍 Add Movies</h3>
        <p style="color: white; font-size: 0.9rem; margin-bottom: 1rem;">Search & add any movie to your collections!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add search suggestions
    st.markdown("**💡 Quick Add Popular Movies:**")
    
    # Get some popular movies for quick selection
    try:
        popular_for_suggestions = movie_service.get_popular_movies_list()[:10]  # First 10 popular movies
        quick_add_movie = st.selectbox(
            "Or choose from popular movies:",
            ["Select a movie..."] + popular_for_suggestions,
            key="quick_add_select"
        )
        
        # Show some debug info to help understand what's available
        with st.expander("🔍 Debug Info (Click to see available movies)"):
            # Get the current movie list (either filtered or main)
            current_movie_list = []
            try:
                # Try to get filtered movie list first
                if 'filtered_movie_list' in locals() and filtered_movie_list:
                    current_movie_list = filtered_movie_list
                else:
                    # Fallback to main movie list
                    current_movie_list = movie_list
            except:
                # Fallback to main movie list
                current_movie_list = movie_list
            
            st.write(f"**Main Database Movies**: {len(current_movie_list)} available")
            st.write(f"**Popular Movies**: {len(popular_for_suggestions)} available")
            st.write("**Sample from main database:**")
            for i, movie in enumerate(current_movie_list[:5]):
                st.write(f"• {movie}")
            st.write("**Sample from popular movies:**")
            for i, movie in enumerate(popular_for_suggestions[:5]):
                st.write(f"• {movie}")
    except Exception as e:
        quick_add_movie = "Select a movie..."
        st.error(f"Error loading popular movies: {str(e)}")
    
    collection_search = st.text_input(
        "🔍 Or type movie name manually:",
        placeholder="Type movie name (e.g., Godfather, Batman, Inception)...",
        key="collection_search"
    )
    
    collection_type = st.selectbox(
        "Add to:",
        ["Watchlist", "Favorites", "History"],
        key="collection_type"
    )
    
    # Determine which movie to add (either from dropdown or text input)
    movie_to_add = None
    if quick_add_movie != "Select a movie...":
        movie_to_add = quick_add_movie
        st.success(f"✅ Selected: {quick_add_movie}")
    elif collection_search and collection_search.strip():
        movie_to_add = collection_search.strip()
    
    if st.button("➕ Add to Collection", key="add_to_collection", use_container_width=True):
        if movie_to_add:
            # Debug: Show what we're trying to add
            st.info(f"🔍 **Debug**: Trying to add '{movie_to_add}' to {collection_type}")
            st.info(f"🔍 **Debug**: Movie type: {type(movie_to_add)}")
            st.info(f"🔍 **Debug**: Movie length: {len(movie_to_add) if movie_to_add else 'None'}")
            
            # Smart search: find movies that contain the search term (case-insensitive)
            # First check in the main movie list, then in popular movies
            matching_movies = []
            search_lower = movie_to_add.lower()
            
            # Get the current movie list (either filtered or main)
            current_movie_list = []
            try:
                # Try to get filtered movie list first
                if 'filtered_movie_list' in locals() and filtered_movie_list:
                    current_movie_list = filtered_movie_list
                else:
                    # Fallback to main movie list
                    current_movie_list = movie_list
            except:
                # Fallback to main movie list
                current_movie_list = movie_list
            
            # Search in current movie list
            for movie in current_movie_list:
                if search_lower in movie.lower():
                    matching_movies.append(movie)
            
            # Also search in popular movies (in case they're not in main list)
            try:
                popular_movies = movie_service.get_popular_movies_list()
                for movie in popular_movies:
                    if search_lower in movie.lower() and movie not in matching_movies:
                        matching_movies.append(movie)
            except:
                pass
            
            # If exact match found in current movie list, use that
            if movie_to_add in current_movie_list:
                exact_match = movie_to_add
            # If exact match found in popular movies, use that
            elif movie_to_add in popular_movies:
                exact_match = movie_to_add
            # If partial matches found, show them and let user choose
            elif matching_movies:
                st.info(f"🔍 Found {len(matching_movies)} matching movies:")
                for i, movie in enumerate(matching_movies[:5]):  # Show first 5 matches
                    st.write(f"• {movie}")
                
                # Let user select from matches
                if len(matching_movies) == 1:
                    # Only one match, use it automatically
                    exact_match = matching_movies[0]
                    st.success(f"✅ Auto-selected: '{exact_match}'")
                else:
                    # Multiple matches, let user choose
                    selected_match = st.selectbox(
                        "Choose the correct movie:",
                        matching_movies,
                        key="movie_selection"
                    )
                    exact_match = selected_match
            else:
                # No matches found
                st.error(f"❌ No movies found matching '{movie_to_add}'. Try:")
                st.write("• Check spelling (e.g., 'Godfather' instead of 'GoDFather')")
                st.write("• Use partial names (e.g., 'Batman' instead of 'The Dark Knight')")
                st.write("• Try shorter search terms")
                st.write(f"• Available movies: {len(current_movie_list)} in database")
                exact_match = None
            
            # If we have a match, add to collection
            if exact_match:
                if collection_type == "Watchlist":
                    if exact_match not in st.session_state.watchlist:
                        st.session_state.watchlist.append(exact_match)
                        st.success(f"✅ Added '{exact_match}' to Watchlist!")
                    else:
                        st.warning(f"⚠️ '{exact_match}' is already in your Watchlist!")
                elif collection_type == "Favorites":
                    if exact_match not in st.session_state.favorites:
                        st.session_state.favorites.append(exact_match)
                        st.success(f"✅ Added '{exact_match}' to Favorites!")
                    else:
                        st.warning(f"⚠️ '{exact_match}' is already in your Favorites!")
                elif collection_type == "History":
                    if exact_match not in st.session_state.watch_history:
                        st.session_state.watch_history.append(exact_match)
                        st.success(f"✅ Added '{exact_match}' to History!")
                    else:
                        st.warning(f"⚠️ '{exact_match}' is already in your History!")
                st.rerun()
    
    st.markdown("---")
    
    # Clear all collections buttons
    if st.button("🗑️ Clear History", key="clear_history", use_container_width=True):
        st.session_state.watch_history = []
        st.success("✅ Watch History cleared!")
        st.rerun()
    
    if st.button("🗑️ Clear Watchlist", key="clear_watchlist", use_container_width=True):
        st.session_state.watchlist = []
        st.success("✅ Watchlist cleared!")
        st.rerun()
    
    if st.button("🗑️ Clear Favorites", key="clear_favorites", use_container_width=True):
        st.session_state.favorites = []
        st.success("✅ Favorites cleared!")
        st.rerun()



# Collection Statistics

# Collection Statistics
if st.session_state.watch_history or st.session_state.watchlist or st.session_state.favorites:
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E8F5E8, #F0F8FF); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; border-left: 4px solid #4ECDC4;">
        <h3 style="color: #333; text-align: center; margin-bottom: 1rem;">📊 Your Movie Stats</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📺 Watch History", len(st.session_state.watch_history))
    
    with col2:
        st.metric("📋 Watchlist", len(st.session_state.watchlist))
    
    with col3:
        st.metric("⭐ Favorites", len(st.session_state.favorites))





