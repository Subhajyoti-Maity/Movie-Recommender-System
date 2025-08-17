import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# TMDB API Configuration
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "8265bd1679663a7ea12ac168da84d2e8")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# App Configuration
APP_TITLE = "🎬 Movie Recommender System"
APP_ICON = "🎬"
PAGE_LAYOUT = "wide"

# Model Configuration
MODEL_PATH = "model"
MOVIE_LIST_FILE = "movie_list.pkl"
SIMILARITY_FILE = "similarity.pkl"

# Performance Configuration
CACHE_SIZE = 100  # Number of movies to cache for filtering
REQUEST_TIMEOUT = 10  # API request timeout in seconds
