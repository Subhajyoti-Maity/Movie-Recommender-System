import pandas as pd
import pickle
import os
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast

def load_existing_model():
    """Load existing model files"""
    try:
        with open('model/movie_list.pkl', 'rb') as f:
            movie_list = pickle.load(f)
        with open('model/similarity.pkl', 'rb') as f:
            similarity = pickle.load(f)
        return movie_list, similarity
    except FileNotFoundError:
        print("Model files not found. Please run generate_model.py first.")
        return None, None

def get_movie_info_from_tmdb(movie_title, api_key=None):
    """Get movie information from TMDB API (optional)"""
    if not api_key:
        print("No TMDB API key provided. Using basic movie info.")
        return None
    
    try:
        # Search for movie
        search_url = f"https://api.themoviedb.org/3/search/movie"
        params = {
            'api_key': api_key,
            'query': movie_title,
            'language': 'en-US'
        }
        
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        results = response.json().get('results', [])
        if results:
            movie_id = results[0]['id']
            
            # Get detailed movie info
            movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            movie_response = requests.get(movie_url, params={'api_key': api_key})
            movie_response.raise_for_status()
            movie_data = movie_response.json()
            
            # Get credits
            credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
            credits_response = requests.get(credits_url, params={'api_key': api_key})
            credits_response.raise_for_status()
            credits_data = credits_response.json()
            
            return {
                'title': movie_data.get('title', movie_title),
                'overview': movie_data.get('overview', ''),
                'genres': [genre['name'] for genre in movie_data.get('genres', [])],
                'keywords': [],  # Would need separate API call
                'cast': [cast['name'] for cast in credits_data.get('cast', [])[:10]],  # Top 10 cast
                'crew': [crew['name'] for crew in credits_data.get('crew', [])[:5]]   # Top 5 crew
            }
    except Exception as e:
        print(f"Error fetching from TMDB API: {e}")
    
    return None

def add_custom_movie(movie_title, overview="", genres=None, keywords=None, cast=None, crew=None):
    """Add a custom movie to the system"""
    if genres is None:
        genres = []
    if keywords is None:
        keywords = []
    if cast is None:
        cast = []
    if crew is None:
        crew = []
    
    # Create movie data
    movie_data = {
        'title': movie_title,
        'overview': overview,
        'genres': genres,
        'keywords': keywords,
        'cast': cast,
        'crew': crew
    }
    
    return movie_data

def update_model_with_new_movies(new_movies):
    """Update the model with new movies"""
    print("Loading existing model...")
    movie_list, similarity = load_existing_model()
    
    if movie_list is None:
        return False
    
    print(f"Current movies in system: {len(movie_list)}")
    
    # Convert new movies to the same format as existing ones
    for movie in new_movies:
        # Create tags by combining all features
        tags = []
        if movie['overview']:
            tags.extend(movie['overview'].split())
        tags.extend(movie['genres'])
        tags.extend(movie['keywords'])
        tags.extend(movie['cast'])
        tags.extend(movie['crew'])
        
        # Add to movie list
        new_row = pd.DataFrame([{
            'movie_id': f"custom_{len(movie_list) + 1}",
            'title': movie['title'],
            'tags': ' '.join(tags)
        }])
        
        movie_list = pd.concat([movie_list, new_row], ignore_index=True)
    
    print(f"Updated movies in system: {len(movie_list)}")
    
    # Recalculate similarity matrix
    print("Recalculating similarity matrix...")
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(movie_list['tags']).toarray()
    new_similarity = cosine_similarity(vector)
    
    # Save updated model
    print("Saving updated model...")
    pickle.dump(movie_list, open('model/movie_list.pkl', 'wb'))
    pickle.dump(new_similarity, open('model/similarity.pkl', 'wb'))
    
    print("Model updated successfully!")
    return True

def main():
    """Main function to add custom movies"""
    print("🎬 Add Custom Movies to Recommender System")
    print("=" * 50)
    
    # Check if model exists
    if not os.path.exists('model/movie_list.pkl'):
        print("Model files not found. Please run generate_model.py first.")
        return
    
    new_movies = []
    
    while True:
        print("\nEnter movie information (or 'done' to finish):")
        title = input("Movie title: ").strip()
        
        if title.lower() == 'done':
            break
        
        overview = input("Overview (optional): ").strip()
        genres_input = input("Genres (comma-separated, optional): ").strip()
        keywords_input = input("Keywords (comma-separated, optional): ").strip()
        cast_input = input("Cast (comma-separated, optional): ").strip()
        crew_input = input("Crew (comma-separated, optional): ").strip()
        
        # Parse inputs
        genres = [g.strip() for g in genres_input.split(',')] if genres_input else []
        keywords = [k.strip() for k in keywords_input.split(',')] if keywords_input else []
        cast = [c.strip() for c in cast_input.split(',')] if cast_input else []
        crew = [c.strip() for c in crew_input.split(',')] if crew_input else []
        
        # Create movie
        movie = add_custom_movie(title, overview, genres, keywords, cast, crew)
        new_movies.append(movie)
        
        print(f"✅ Added: {title}")
    
    if new_movies:
        print(f"\nAdding {len(new_movies)} new movies to the system...")
        if update_model_with_new_movies(new_movies):
            print("🎉 Custom movies added successfully!")
            print("You can now restart the Streamlit app to see the new movies.")
        else:
            print("❌ Failed to add custom movies.")
    else:
        print("No movies to add.")

if __name__ == "__main__":
    main()
